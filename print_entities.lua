-- Start iteration over all entities
local entity = Entities:First()

-- Loop through all entities
while entity do
    print("Name: " .. entity:GetName())
    print("Classname: " .. entity:GetClassname())

    -- Move to the next entity
    entity = Entities:Next(entity)
end