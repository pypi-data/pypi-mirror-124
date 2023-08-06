from __future__ import annotations

import functools
from collections import defaultdict, deque
from contextvars import ContextVar
from typing import (
    Any,
    ContextManager,
    DefaultDict,
    Deque,
    Dict,
    List,
    Mapping,
    Optional,
    Tuple,
    Union,
    cast,
)

from di._dag import topsort
from di._inspect import is_async_gen_callable, is_coroutine_callable
from di._local_scope_context import LocalScopeContext
from di._state import ContainerState
from di._task import AsyncTask, SyncTask, Task
from di.exceptions import (
    DependencyRegistryError,
    DuplicateScopeError,
    ScopeViolationError,
    UnknownScopeError,
)
from di.executors import DefaultExecutor
from di.types import FusedContextManager
from di.types.dependencies import DependantProtocol, DependencyParameter
from di.types.executor import AsyncExecutor, SyncExecutor
from di.types.executor import Task as ExecutorTask
from di.types.providers import (
    DependencyProvider,
    DependencyProviderType,
    DependencyType,
)
from di.types.scopes import Scope
from di.types.solved import SolvedDependency

Dependency = Any


class Container:
    _context: ContextVar[ContainerState]
    _executor: Union[AsyncExecutor, SyncExecutor]

    def __init__(
        self,
        *,
        default_scope: Scope = None,
        executor: Optional[Union[AsyncExecutor, SyncExecutor]] = None,
    ) -> None:
        self._context = ContextVar("context")
        state = ContainerState()
        state.cached_values.add_scope("container")
        state.cached_values.set(Container, self, scope="container")
        self._context.set(state)
        self._executor = executor or DefaultExecutor()
        self._default_scope = default_scope

    @property
    def _state(self) -> ContainerState:
        return self._context.get()

    @property
    def scopes(self) -> List[Scope]:
        return self._state.scopes

    def enter_global_scope(self, scope: Scope) -> FusedContextManager[None]:
        """Enter a global scope that is share amongst threads and coroutines.

        If you enter a global scope in one thread / coroutine, it will propagate to others.
        """
        return self._state.enter_scope(scope)

    def enter_local_scope(self, scope: Scope) -> FusedContextManager[None]:
        """Enter a local scope that is localized to the current thread or coroutine.

        If you enter a global scope in one thread / coroutine, it will NOT propagate to others.
        """
        if scope in self._state.stacks:
            raise DuplicateScopeError(f"Scope {scope} has already been entered!")
        return LocalScopeContext(self._context, scope)

    def bind(
        self,
        provider: DependantProtocol[DependencyType],
        dependency: DependencyProviderType[DependencyType],
    ) -> ContextManager[None]:
        """Bind a new dependency provider for a given dependency.

        This can be used as a function (for a permanent bind, cleared when `scope` is exited)
        or as a context manager (the bind will be cleared when the context manager exits).

        Binds are only identified by the identity of the callable and do not take into account
        the scope or any other data from the dependency they are replacing.

        The `scope` parameter determines the scope for the bind itself.
        The bind will be automatically cleared when that scope is exited.
        If no scope is provided, the current scope is used.
        """
        return self._state.bind(provider=provider, dependency=dependency)

    def __contains__(self, o: object) -> bool:
        return o in self._state.binds

    def __getitem__(
        self, provider: DependencyProviderType[DependencyType]
    ) -> DependantProtocol[DependencyType]:
        return self._state.binds[provider]

    def solve(
        self,
        dependency: DependantProtocol[DependencyType],
    ) -> SolvedDependency[DependencyType]:
        """Solve a dependency.

        Returns a SolvedDependency that can be executed to get the dependency's value.

        The `siblings` paramter can be used to pass additional dependencies that should be executed
        that aren't strictly needed to solve `dependency`.
        """

        if dependency.call in self._state.binds:
            dependency = self._state.binds[dependency.call]

        param_graph: Dict[
            DependantProtocol[Any],
            List[DependencyParameter[DependantProtocol[Any]]],
        ] = {}

        dep_registry: Dict[DependantProtocol[Any], DependantProtocol[Any]] = {}

        dep_dag: Dict[DependantProtocol[Any], List[DependantProtocol[Any]]] = {}

        def get_params(
            dep: DependantProtocol[Any],
        ) -> List[DependencyParameter[DependantProtocol[Any]]]:
            params = dep.get_dependencies().copy()
            for idx, param in enumerate(params):
                assert param.dependency.call is not None
                if param.dependency.call in self._state.binds:
                    params[idx] = DependencyParameter[Any](
                        dependency=self._state.binds[param.dependency.call],
                        parameter=param.parameter,
                    )
            return params

        def check_equivalent(dep: DependantProtocol[Any]):
            if dep in dep_registry and dep.scope != dep_registry[dep].scope:
                raise DependencyRegistryError(
                    f"The dependencies {dep} and {dep_registry[dep]}"
                    " have the same lookup (__hash__ and __eq__) but have different scopes"
                    f" ({dep.scope} and {dep_registry[dep].scope} respectively)"
                    " This is likely a mistake, but you can override this behavior by either:"
                    "\n  1. Wrapping the function in another function or subclassing the class such"
                    " that they now are considered different dependencies"
                    "\n  2. Use a custom implemetnation of DependantProtocol that changes the meaning"
                    " or computation of __hash__ and/or __eq__"
                )

        q: Deque[DependantProtocol[Any]] = deque([dependency])
        while q:
            dep = q.popleft()
            if dep in dep_registry:
                check_equivalent(dep)
            else:
                dep_registry[dep] = dep
                params = get_params(dep)
                param_graph[dep] = params
                dep_dag[dep] = []
                for param in params:
                    subdep = param.dependency
                    dep_dag[dep].append(subdep)
                    if subdep not in dep_registry:
                        q.append(subdep)
        tasks = self._build_tasks(param_graph, topsort(dep_dag))
        dependency_dag = {dep: set(subdeps) for dep, subdeps in dep_dag.items()}
        # we store several things:
        # - the dependency itself
        # - dag, which includes parameter information and is public
        # - _dependency_dag: same as dag but without param info and w/o repeated params (so a set instead of a list)
        # - _tasks: a mapping of dependency to tasks
        return SolvedDependency(
            dependency=dependency,
            dag=param_graph,
            _dependency_dag=dependency_dag,
            _tasks=tasks,
        )

    def _build_tasks(
        self,
        dag: Dict[
            DependantProtocol[Any],
            List[DependencyParameter[DependantProtocol[Any]]],
        ],
        topsorted: List[DependantProtocol[Any]],
    ) -> Dict[DependantProtocol[Any], Union[AsyncTask[Any], SyncTask[Any]]]:
        tasks: Dict[DependantProtocol[Any], Union[AsyncTask[Any], SyncTask[Any]]] = {}
        for dep in reversed(topsorted):
            tasks[dep] = self._build_task(dep, tasks, dag)
        return tasks

    def _build_task(
        self,
        dependency: DependantProtocol[Any],
        tasks: Dict[DependantProtocol[Any], Union[AsyncTask[Any], SyncTask[Any]]],
        dag: Dict[
            DependantProtocol[Any],
            List[DependencyParameter[DependantProtocol[Any]]],
        ],
    ) -> Union[AsyncTask[Any], SyncTask[Any]]:

        task_dependencies: List[DependencyParameter[Task[Any]]] = [
            DependencyParameter(
                dependency=tasks[param.dependency], parameter=param.parameter
            )
            for param in dag[dependency]
        ]

        if is_async_gen_callable(dependency.call) or is_coroutine_callable(
            dependency.call
        ):
            return AsyncTask(dependant=dependency, dependencies=task_dependencies)
        else:
            return SyncTask(dependant=dependency, dependencies=task_dependencies)

    def _validate_scopes(self, solved: SolvedDependency[Dependency]) -> None:
        """Validate that dependencies all have a valid scope and
        that dependencies only depend on outer scopes or their own scope.
        """
        scopes: Dict[Scope, int] = {
            scope: idx
            for idx, scope in enumerate(reversed(self._state.scopes + [None]))
        }

        def check_is_inner(
            dep: DependantProtocol[Any], subdep: DependantProtocol[Any]
        ) -> None:
            if scopes[dep.scope] > scopes[subdep.scope]:
                raise ScopeViolationError(
                    f"{dep} cannot depend on {subdep} because {subdep}'s"
                    f" scope ({subdep.scope}) is narrower than {dep}'s scope ({dep.scope})"
                )

        def check_scope(dep: DependantProtocol[Any]) -> None:
            if dep.scope not in scopes:
                raise UnknownScopeError(
                    f"Dependency{dep} has an unknown scope {dep.scope}."
                    f" Did you forget to enter the {dep.scope} scope?"
                )

        for dep, params in solved.dag.items():
            check_scope(dep)
            for param in params:
                subdep = param.dependency
                check_scope(subdep)
                check_is_inner(dep, subdep)

    def _prepare_execution(
        self,
        solved: SolvedDependency[Any],
        *,
        validate_scopes: bool = True,
        values: Optional[Mapping[DependencyProvider, Any]] = None,
    ) -> Tuple[Dict[DependantProtocol[Any], Any], List[ExecutorTask]]:
        results: Dict[DependantProtocol[Any], Any] = {}
        values = values or {}
        if validate_scopes:
            self._validate_scopes(solved)

        tasks = solved._tasks

        # Build a DAG of Tasks that we actually need to execute
        # this allows us to prune subtrees that will come from cached values
        unvisited = deque([solved.dependency])
        # Make DAG values a set to account for dependencies that depend on the the same
        # sub dependency in more than one param (`def func(a: A, a_again: A)`)
        dag: Dict[DependantProtocol[Any], List[DependantProtocol[Any]]] = {}
        dependant_dag: DefaultDict[
            DependantProtocol[Any], List[Task[Any]]
        ] = defaultdict(list)
        while unvisited:
            dep = unvisited.pop()
            if dep in dag:
                continue
            task = tasks[dep]
            # task the dependency is cached or was provided by value
            # we don't need to compute it or any of it's dependencies
            if not task.from_cache_or_values(self._state, results, values):
                # otherwise, we add it to our DAG and visit it's children
                dag[dep] = []
                for subdep in solved._dependency_dag[dep]:
                    if not tasks[subdep].from_cache_or_values(
                        self._state, results, values
                    ):
                        dependant_dag[subdep].append(tasks[dep])
                        dag[dep].append(subdep)
                        if subdep not in dag:
                            unvisited.append(subdep)

        dependency_counts = {dep: len(subdeps) for dep, subdeps in dag.items()}

        leafs: List[ExecutorTask] = []
        for dep, depcount in dependency_counts.items():
            if depcount == 0:
                leaf = functools.partial(
                    tasks[dep].compute,
                    state=self._state,
                    results=results,
                    values=values,
                    dependency_counts=dependency_counts,
                    dependants=dependant_dag,
                )
                leafs.append(leaf)  # type: ignore[arg-type] # beacuse of partial

        return results, leafs

    def execute_sync(
        self,
        solved: SolvedDependency[DependencyType],
        *,
        validate_scopes: bool = True,
        values: Optional[Mapping[DependencyProvider, Any]] = None,
    ) -> DependencyType:
        """Execute an already solved dependency.

        If you are not dynamically changing scopes, you can run once with `validate_scopes=True`
        and then disable scope validation in subsequent runs with `validate_scope=False`.
        """
        with self.enter_local_scope(self._default_scope):
            results, queue = self._prepare_execution(
                solved, validate_scopes=validate_scopes, values=values
            )
            if not hasattr(self._executor, "execute_sync"):
                raise TypeError(
                    "execute_sync requires an executor implementing the SyncExecutor protocol"
                )
            executor = cast(SyncExecutor, self._executor)
            if queue:
                executor.execute_sync(queue)
            return results[solved.dependency]

    async def execute_async(
        self,
        solved: SolvedDependency[DependencyType],
        *,
        validate_scopes: bool = True,
        values: Optional[Mapping[DependencyProvider, Any]] = None,
    ) -> DependencyType:
        """Execute an already solved dependency.

        If you are not dynamically changing scopes, you can run once with `validate_scopes=True`
        and then disable scope validation in subsequent runs with `validate_scope=False`.
        """
        async with self.enter_local_scope(self._default_scope):
            results, queue = self._prepare_execution(
                solved, validate_scopes=validate_scopes, values=values
            )
            if not hasattr(self._executor, "execute_async"):
                raise TypeError(
                    "execute_async requires an executor implementing the AsyncExecutor protocol"
                )
            executor = cast(AsyncExecutor, self._executor)
            if queue:
                await executor.execute_async(queue)
            return results[solved.dependency]
