-- Find the player entity
local player = Entities:GetLocalPlayer()

-- Define the Think function
function PlayerThinkFunction()
    print("Player think function running every 5 seconds")
    
    -- Run the Think function again after 5 seconds
    return 5.0
end

-- Override the player's Spawn function
-- function player:Spawn()
--     player:Spawn()
    player:SetThink(PlayerThinkFunction, "player_think", 5)
-- end


