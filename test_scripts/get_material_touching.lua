-- Define a function to trace down from an entity and get the material
function GetMaterialEntityIsTouching(entity)
    -- Get the entity's current position
    local entityPos = entity:GetOrigin()

    -- Define a trace table to hold the result
    local traceTable = {
        startpos = entityPos,             -- Start from the entity's origin
        endpos = entityPos - Vector(100, 100, 1000),  -- Trace downward (100 units down)
        mask = MASK_NPCSOLID,                -- Only trace against solid objects
        ignore = entity,                  -- Ignore the entity itself in the trace
    }

    -- Perform the trace
    TraceLine(traceTable)

    -- Check if we hit something
    if traceTable.hit then
        -- Get the surface material name (if available)
        local materialName = traceTable.CBaseEntity
        print("Entity is touching material:", materialName)
        return materialName
        -- for k,v in pairs(traceTable) do
        --     print( k,v )
        -- end
    else
        print("Entity is not touching any material!")
        return nil
    end
end

-- Example: Get the material the player is touching
local player = Entities:FindByClassname(null, "hlvr_piano")
if player then
    GetMaterialEntityIsTouching(player)
else
    print("Player entity not found!")
end
