--[[
    Installation
    - Create the directory game/hlvr/vscripts/scripts

    - Copy this script into this new folder.

    - If you want to run it automatically add a "script_reload_code your_script.lua" to hlvr/cfg/skill.cfg or some or CFG that is automatically loaded.

    - Load up the game, and you're done!

    - To run it manually open the console in game and run "script_reload_code your_script.lua"
]]

local modelname = "models/hands/alyx_hand_right.vmdl"
local classname = "hl_prop_vr_hand"

WatchEnt = Entities:GetLocalPlayer()

LineLength = 1
Timer = 1 / 30
DebugLineColor = Vector(252, 186, 3)

local dirTable = {
    fingertip_thumb = "f",
    fingertip_index = "l",
    fingertip_middle = "l",
    fingertip_ring = "l",
    fingertip_pinky = "f"
}

function FindEntityByClassnameAndModel(classname, modelname)
    local ents = Entities:FindAllByModel(modelname)
    local ent = nil
    for _, e in pairs(ents) do
        if (e:GetClassname() == classname) then
            ent = e
            break
        end
    end

    return ent
end

function TableToJson(tbl)
    local function serialize(tbl)
        local result = {}

        -- Check if the table is an array (has numeric keys)
        local isArray = (#tbl > 0)

        for k, v in pairs(tbl) do
            local key = ""
            if not isArray then
                if type(k) == "string" then
                    key = '"' .. k .. '":'
                else
                    key = ''
                end
            end

            local value
            if type(v) == "table" then
                value = serialize(v)
            elseif type(v) == "string" then
                if(v == "None") then
                    value = 'null'
                else
                    value = '"' .. v .. '"'
                end
            elseif type(v) == "boolean" or type(v) == "number" then
                value = tostring(v)
            else
                value = 'null'
            end

            table.insert(result, key .. value)
        end

        if isArray then
            return "[" .. table.concat(result, ",") .. "]"
        else
            return "{" .. table.concat(result, ",") .. "}"
        end
    end

    return serialize(tbl)
end

Prev_hitEnts_json = nil

function DrawFingetipsNormal()
    local hitEnts = {}

    for finger, dir in pairs(dirTable) do
        local attach_id = HandEnt:ScriptLookupAttachment(finger)
        local fingertipPos = HandEnt:GetAttachmentOrigin(attach_id)
        local fingerAngles = HandEnt:GetAttachmentAngles(attach_id)

        local fingertipVec = QAngle(fingerAngles.x, fingerAngles.y, fingerAngles.z)
        if (dir == "f") then
            fingertipVec = fingertipVec:Forward()
        elseif (dir == "l") then
            fingertipVec = fingertipVec:Left()
        end
        fingertipVec = fingertipVec:Normalized()

        local pointA = fingertipPos
        local pointB = fingertipPos + fingertipVec * LineLength

        local traceTable = {
            startpos = pointA,
            endpos = pointB,
            ignore = WatchEnt,
            mask = MASK_SOLID
        }
        DebugDrawLine(fingertipPos, fingertipPos + fingertipVec * LineLength, DebugLineColor.x, DebugLineColor.y, DebugLineColor.z, false, Timer)
        TraceLine(traceTable)

        local t = {
            fingername = finger,
            classname = "None",
            modelname = "None"
        }
        if traceTable.hit then
            local ent = traceTable.enthit
            local entClassname = ent:GetClassname()
            if(entClassname  ~= "worldent") then
                t.classname = entClassname
                t.modelname = ent:GetModelName()
            end
        end
        table.insert(hitEnts, t)
    end

    local hitEnts_json= TableToJson(hitEnts)

    if hitEnts_json ~= Prev_hitEnts_json then
        print("[WeArt_s] " .. hitEnts_json .. " [WeArt_e]")
        Prev_hitEnts_json = hitEnts_json
    end

    --DebugDrawSphere(fingertipPos, DebugLineColor, 255, sphere_rad, false, Timer)
    -- DebugDrawSphere(Entities:FindByModel(null, "models/props/chair_wood_1.vmdl"):GetCenter(), DebugLineColor, 255, sphere_rad, false, Timer)

    return Timer
end

HandEnt = FindEntityByClassnameAndModel(classname, modelname)

WatchEnt:SetThink(DrawFingetipsNormal, self, Timer)
