local hand = Entities:FindByClassname(null, "hl_prop_vr_hand")

for key, value in pairs(getmetatable(hand)) do
    print(key, value)
end