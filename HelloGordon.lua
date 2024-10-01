if player_spawn_ev ~= nil then
	StopListeningToGameEvent(player_spawn_ev)
end

player_spawn_ev = ListenToGameEvent('player_spawn', function(info)
	if not IsServer() then return end
    print( "miso" )
end, nil)
