---
title: Server
---
```mermaid
classDiagram 

class Agent {
    __firstArenaRx
    robot
    __firepath
    __playerKeyToAttribute
    __gameKeyToAttribute
    __sourcesDir
    __playerReqBuf
    __onAttributeChangeCallbacks
   __init__(self,playerId:str or None=None, arena:str or None=None, username:str or None=None, password:str or None=None, server:str or None=None, port:int=1883, imgOutputPath:str or None="img.jpeg", autoconnect:bool=True, waitArenaConnection:bool=True, verbosity:int=3, robotId:str or None="_", welcomePrint:bool=True, sourcesdir:str or None=None) 
   connect(self) 
   disconnect(self) 
   isConnectedToRobot(self) 
   isConnectedToArena(self) 
   update(self,enableSleep=True) 
   fire(self,enable:bool=True, firepath:Callable[[int],int] or None=None) 
   accelerate(self,ax:float,ay:float) 
   move(self,dx:int,dy:int) 
   moveTowards(self,x:int,y:int) 
   lookAt(self,dir:int) 
   ruleArena(self, attributeName:str, attributeValue:Any) 
   rulePlayer(self, agentId:str, attributeName:str, attributeValue:Any) 
   setColor(self, r:int, g:int, b:int) 
   addEventListener(self,attributeName:str, callback:Callable[[Any,str,Any,Any], None]) 
   print(self) 
   _onRobotIdChanged(self, valueBefore:int, valueAfter:int) 
   _onUpdated(self, eventSrc:Any, eventName:str, eventValue:Any) 
   __afterRobotConnected(self) 
   _onRobotConnected(self, eventSrc:Any, eventName:str, playerState: dict[str, Any]) 
   _onPlayerChanged(self, eventSrc:Any, eventName:str, playerState: dict[str, Any]) 
   _onArenaChanged(self, eventSrc:Any, eventName:str, arenaState:dict[str,Any]) 
   __run__(filepath:str="settings.json", agentInfos=None) 
}
class IAgent {
    vx
    game
    vy
    distance
    color
    nDeath
    isFiring
    range
    gridRows
    dir
    life
    robot
    score
    infoPlayer
    rank
    robots
    nKill
    map
    playerId
    nCollision
    clientId
    ammo
    gridColumns
    pose
    players
    isGamePaused
    profile
    nHitFire
    team
    nFire
    robotId
    nMove
    dtCreated
    nExe
    x
    infoArena
    y
   __init__(self) 
   connect(self) 
   disconnect(self) 
   isConnectedToRobot(self) 
   isConnectedToArena(self) 
   update(self) 
   fire(self,enable:bool=True, firepath:Callable[[int],int] or None=None) 
   accelerate(self,ax:float,ay:float) 
   move(self,dx:int,dy:int) 
   moveTowards(self,x:int,y:int) 
   lookAt(self,dir:int) 
   ruleArena(self, attributeName:str, attributeValue:Any) 
   rulePlayer(self, agentId:str, attributeName:str, attributeValue:Any) 
   setColor(self, r:int, g:int, b:int) 
   addEventListener(self,attributeName:str, callback:Callable[[Any,str,Any,Any], None]) 
   _onRobotIdChanged(self, valueBefore:int, valueAfter:int) 
   _onXChanged(self, valueBefore:int, valueAfter:int) 
   _onYChanged(self, valueBefore:int, valueAfter:int) 
   _onDirChanged(self, valueBefore:int, valueAfter:int) 
   _onAmmoChanged(self, valueBefore:int, valueAfter:int) 
   _onLifeChanged(self, valueBefore:int, valueAfter:int) 
   _onDistanceChanged(self, valueBefore:int, valueAfter:int) 
   _onRangeChanged(self, valueBefore:dict[str,Any], valueAfter:dict[str,Any]) 
   _onDead(self, valueBefore:int, valueAfter:int) 
   _onKill(self, valueBefore:int, valueAfter:int) 
   _onMove(self, valueBefore:int, valueAfter:int) 
   _onPublicMessageReceived(self, valueBefore:str, valueAfter:str) 
   _onPrivateMessageReceived(self, valueBefore:str, valueAfter:str) 
   _onPlayerNumberChanged(self, valueBefore:list[str], valueAfter:list[str]) 
   _onRobotNumberChanged(self, valueBefore:list[str], valueAfter:list[str]) 
   _onGamePauseChanged(self, valueBefore:bool, valueAfter:bool) 
   _onGridColumnsChanged(self, valueBefore:int, valueAfter:int) 
   _onGridRowsChanged(self, valueBefore:int, valueAfter:int) 
}
class Manager {
    __game_running
    __TIME_LIMIT
    _logger
    __paused_time
    __map
    __start_time
    _robot
    __state_machine
    __rules
    __registered_players
    __state_machine
   __init__(self, nom, arene, username, password) 
   on_update(self, other, event, value) 
   __all_players_dead(self) 
   __timer_running(self) 
   game_loop_running(self) 
   all_players_connected(self) 
   get_rules(self) 
   registered_players(self) 
   game_loop(self) 
   __update_rules(self, rules: Dict[str, Any]) 
   set_pause(self, pause: bool) 
   set_map(self, _map: List[List[int]]) 
   __get_player(self, player_id: Union[int | str]) 
   kill_player(self, player_id: int) 
   register_player(self, player: Player) 
   unregister_player(self, player_id: str) 
   update_player_stats(self, player: Union[int | str]) 
   update_players(self, *args, **kwargs) 
   __str__(self) 
   display(self, message: str) 
   state(self) 
   __game_infos(self) 
   __timers(self) 
   game_running(self) 
   game_running(self, value: bool) 
   __update_timers(self) 
   restart(self) 
   stop(self) 
   mod_game(self, key: str, value: Any) 
}
class IManager {
    __last_loop_time
   __init__(self, nom, arene, username, password) 
   last_loop_time(self) 
   game_loop(self) 
   on_update(self, other, event, value) 
   get_rules(self) 
   all_players_connected(self) 
   set_pause(self, pause: bool) 
   set_map(self, _map: List[List[int]]) 
   kill_player(self, player_id: int) 
   register_player(self, player: Player) 
   unregister_player(self, player_id: int) 
   update_players(self, *args, **kwargs) 
   update_player_stats(self, player: Player) 
   state(self) 
   display(self, text) 
   game_loop_running(self) 
   __del__(self) 
   __enter__(self) 
   __exit__(self, exc_type, exc_val, exc_tb) 
}
class ABC {
    metadata
}
class Direction {
    NORTH
    NORTHNORTHEAST
    NORTHEAST
    EAST
    EASTSOUTHEAST
    SOUTHEAST
    SOUTHSOUTHEAST
    SOUTH
    SOUTHSOUTHWEST
    SOUTWEST
    WEST
    NORTHWEST
    NORTHNORTHWEST
   from_rotation(angle: int) 
}
class Player {
    score
    name
    x
    health
    y
    inventory
    direction
    __tablename__
    id
    created_at
    updated_at
    name
    health
    inventory
    x
    y
    direction
    score
    known_map
   serialize(self) 
   __init__(self, name: str, **kw: Any) 
   __repr__(self) 
   __str__(self) 
   add_score(self, score: float) 
   sub_score(self, score: float) 
   add_health(self, health: int) 
   sub_health(self, health: int) 
   add_item(self, item: Dict) 
   remove_item(self, item: Dict) 
   set_position(self, x: int, y: int) 
}
class State {
    _agent
    _logger
   __init__(self, agent: IManager) 
   handle(self) 
   _on_handle(self) 
}
class IState {
   handle(self) 
}
class BaseState {
    __context
   name(self) 
   set_context(self, context: StateMachine) 
   switch_state(self, state: StateEnum) 
}
class StateMachine {
    __lock
    __agent
    __actual_state
    _logger
    __allowed_switches
    __states
   __init__(self, controller: IManager) 
   define_states(self, states: tuple, links: List[Tuple[StateEnum, StateEnum]],
                      initial_state: StateEnum = None) 
   state(self) 
   set_actual_state(self, requested_state: StateEnum) 
   handle(self) 
   __add_state(self, state: BaseState.__class__) 
   __define_states_links(self, connexions: List[Tuple[StateEnum, StateEnum]]) 
   __is_allowed(self, new_state: StateEnum) 

}
class EndGame {
   name(self) 
   _on_handle(self) 
}
class InGame {
    __loop_start_time
   name(self) 
   _on_handle(self) 
   __unpause(self) 
   __handle_players_events(self) 
   __handle_game_events(self) 
   __update(self) 
}
class StateEnum {
    WAIT_PLAYERS_CONNEXION
    WAIT_PLAYERS
    IN_GAME
    END_GAME
    WAIT_GAME_START
}
class WaitGameStart {
   name(self) 
   _on_handle(self) 
}
class WaitPlayers {
   name(self) 
   _on_handle(self) 
   __wait_all_players(self) 
   __start_game(self) 
}
class WaitPlayersConnexion {
   name(self) 
   _on_handle(self) 
}

BaseState --> WaitPlayers
BaseState --> InGame
BaseState --> EndGame
WaitPlayers --> WaitGameStart
WaitPlayers --> WaitPlayersConnexion



```
