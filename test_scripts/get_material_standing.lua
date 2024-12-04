-- Function to create and configure the env_player_surface_trigger
function CreateSurfaceTrigger(position)
    -- Spawn the env_player_surface_trigger entity at the given position
    local surfaceTrigger = SpawnEntityFromTableSynchronous("env_player_surface_trigger", {
        origin = position,
        targetname = "my_surface_trigger",  -- Name for the entity
        filterclass = "player",             -- Only trigger for the player class
    })

    -- local ent = Entities:FindByName(null, "my_surface_trigger")
    -- print(type(ent))

    -- Check if the entity was successfully created
    if surfaceTrigger then
        print("env_player_surface_trigger created at position: " .. tostring(position))

        -- Set up output events to fire Lua functions when player touches or stops touching a surface
        surfaceTrigger:FireOutput("OnStartTouch", OnSurfaceTouchStart(), surfaceTrigger, nil, 0)
        surfaceTrigger:FireOutput("OnEndTouch", OnSurfaceTouchEnd(), surfaceTrigger, nil, 0)

        return surfaceTrigger
    else
        print("Failed to create env_player_surface_trigger")
        return nil
    end
end

-- Define the function that runs when the player touches the surface
function OnSurfaceTouchStart(trigger)
    -- Get the material of the surface being touched
    if trigger then
        local material = trigger.material or "unknown"
        print("Player has started touching surface with material: " .. material)
    else 
        print("No trigger found!")
    end
end

-- Define the function that runs when the player stops touching the surface
function OnSurfaceTouchEnd(trigger)
    if trigger then 
        local material = trigger.material or "unknown"
        print("Player has stopped touching surface with material: " .. material)
    else
        print("No trigger found!")
    end
end

-- Example usage: Create a surface trigger at a specific location
local playerPos = Entities:GetLocalPlayer():GetOrigin()
CreateSurfaceTrigger(playerPos)
