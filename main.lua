
repeat wait() until game:IsLoaded() and game.Players.LocalPlayer:FindFirstChild("DataLoaded")
local headers = {
    ["Content-Type"] = "application/json"
}

local HttpService = game:GetService("HttpService")
local requestt = http_request or request or syn.request
local player = game.Players.LocalPlayer
repeat task.wait()
    local playerGui = game:GetService("Players").LocalPlayer.PlayerGui
    if playerGui:FindFirstChild("Main") and playerGui.Main:FindFirstChild("ChooseTeam") then
        local piratesButtonFrame = playerGui.Main.ChooseTeam.Container.Marines.Frame

        if piratesButtonFrame:FindFirstChild("TextButton") then 
            for _, connection in pairs(getconnections(piratesButtonFrame.TextButton.Activated)) do
                connection.Function()
            end
        end
    end
until game.Players.LocalPlayer.Team ~= nil

function formatNumber(v)
    return tostring(v):reverse():gsub("%d%d%d", "%1,"):reverse():gsub("^,", "")
end
function checkweapon() 
    sw = {}
    local args = game:GetService("ReplicatedStorage"):WaitForChild("Remotes"):WaitForChild("CommF_"):InvokeServer("getInventory")
    for i,v in pairs(args) do 
        if v.Type == "Sword" and (v.Rarity == 3 or v.Rarity == 4) then
            table.insert(sw, v.Name)
        end
    end
    return table.concat(sw, ",")
end
function checkgun() 
    sw = {}
    local args = game:GetService("ReplicatedStorage"):WaitForChild("Remotes"):WaitForChild("CommF_"):InvokeServer("getInventory")
    for i,v in pairs(args) do 
        if v.Type == "Gun" and (v.Rarity == 3 or v.Rarity == 4) then
            table.insert(sw, v.Name)
        end
    end
    return table.concat(sw, ",")
end
function checkfruit() 
    fruit = {}
    local args = game:GetService("ReplicatedStorage"):WaitForChild("Remotes"):WaitForChild("CommF_"):InvokeServer("getInventory")
    for i,v in pairs(args) do 
        if v.Type == "Blox Fruit" then
            if v.Rarity == 3 or v.Rarity == 4 then 
                table.insert(fruit, v.Name)
            end
        end
    end
    return table.concat(fruit, ",")
end
local getawaken = (function()
    local v99 = {}
    local v100 = game.ReplicatedStorage.Remotes.CommF_:InvokeServer("getAwakenedAbilities")
    if v100 then
        for _, k90 in pairs(v100) do
            wait()
            if k90.Awakened then
                table.insert(v99, k90.Key)
            end
        end
    end
    return table.concat(v99, ", ")
end)
function checkmelee()
    local checkmelee = {}
    if game.ReplicatedStorage.Remotes.CommF_:InvokeServer("BuySharkmanKarate", true) == 1 then
        table.insert(checkmelee, "Sharkman Karate")
    end
    if game.ReplicatedStorage.Remotes.CommF_:InvokeServer("BuyDeathStep", true) == 1 then
        table.insert(checkmelee, "Death Step")
    end
    if game.ReplicatedStorage.Remotes.CommF_:InvokeServer("BuyElectricClaw", true) == 1 then
        table.insert(checkmelee, "Electric Claw")
    end
    if game.ReplicatedStorage.Remotes.CommF_:InvokeServer("BuyDragonTalon", true) == 1 then
        table.insert(checkmelee, "Dragon Talon")
    end
    if game.ReplicatedStorage.Remotes.CommF_:InvokeServer("BuySuperhuman", true) == 1 then
        table.insert(checkmelee, "Superhuman")
    end
    if game.ReplicatedStorage.Remotes.CommF_:InvokeServer("BuyGodhuman", true) == 1 then
        table.insert(checkmelee, "Godhuman")
    end
    return table.concat(checkmelee, ", ")
end
function checkgatcan()
    local a = game:GetService("ReplicatedStorage"):WaitForChild("Remotes"):WaitForChild("CommF_"):InvokeServer("CheckTempleDoor")
    if a then 
        return true
    else 
        return false 
    end
end
function checkgatcan2()
    cac = {}
    if checkgatcan() then 
        table.insert(cac, "The lever has been pulled") 
    else 
        table.insert(cac, "Not yet pulled lever")
    end
    return table.concat(cac)
end
function checkmirrorvamu()
    checkcheck = {}
    for i, v in pairs(game:GetService("ReplicatedStorage"):WaitForChild("Remotes"):WaitForChild("CommF_"):InvokeServer("getInventory")) do
        if v.Name == "Mirror Fractal" or  v.Name == "Valkyrie Helm" then 
            table.insert(checkcheck, v.Name)
        end
    end
    return table.concat(checkcheck, " & ")
end
function checkrace()
    race = {}
    local v113 = game.ReplicatedStorage.Remotes.CommF_:InvokeServer("Wenlocktoad", "1")
    local v111 = game.ReplicatedStorage.Remotes.CommF_:InvokeServer("Alchemist", "1")
    if game.Players.LocalPlayer.Character:FindFirstChild("RaceTransformed") then
        table.insert(race, game.Players.LocalPlayer.Data.Race.Value.." V4")
    end
    if v113 == -2 and not game.Players.LocalPlayer.Character:FindFirstChild("RaceTransformed") then 
        table.insert(race, game.Players.LocalPlayer.Data.Race.Value.." V3")
    end
    if v111 == -2 and not game.Players.LocalPlayer.Character:FindFirstChild("RaceTransformed") then 
        table.insert(race, game.Players.LocalPlayer.Data.Race.Value.." V2") 
    end 
    if not game:GetService("Players").LocalPlayer.Data.Race:FindFirstChild("Evolved") then
        table.insert(race, game.Players.LocalPlayer.Data.Race.Value.." V1")
    end
    return table.concat(race)
end
function checkmaterial()
    local a = {}
    local inventory = game:GetService("ReplicatedStorage"):WaitForChild("Remotes"):WaitForChild("CommF_"):InvokeServer("getInventory")
    for i, v in pairs(inventory) do
        if v.Type == "Material" then
            table.insert(a, tostring(v.Name) .. " x" .. tostring(v.Count))
        end
    end
    return table.concat(a, ", ")
end
function checkmasterydf()
    local mas = 0
    for i,v in pairs(game.Players.LocalPlayer.Backpack:GetChildren()) do
        if v:IsA("Tool") and v.ToolTip == "Blox Fruit" then
            mas = v.Level.Value
        end
    end
    return mas
end

function Webhook()
    local ddr = game:GetService("Players").LocalPlayer.Data.DevilFruit.Value
    local level = game:GetService("Players").LocalPlayer.Data.Level.Value
    local beli = formatNumber(game:GetService("Players").LocalPlayer.Data.Beli.Value)
    local fragment = formatNumber(game:GetService("Players").LocalPlayer.Data.Fragments.Value)
    local player = game.Players.LocalPlayer

    local playerStatsField = {
        ["name"] = 'Player Stats',
        ["value"] = "• Username: ||" .. player.Name .. "||\n" ..
                    "• Level: " ..level.. "\n" ..
                    "• Beli: " .. beli .. "\n" ..
                    "• Fragment: " .. fragment .. "\n" ..
                    "• Fruit Using: " .. ddr .. "\n" ..
                    "• Race: " .. checkrace(),
        ["inline"] = false
    }

    local inventoryField = {
        ["name"] = 'Inventory',
        ["value"] = "• List Fruit: " .. checkfruit() .. "\n" ..
                    "• Material: " .. checkmaterial() .. "\n" .. "• Mirror Fractal: " .. checkmirrorvamu(),
        ["inline"] = false
    }

    local combatField = {
        ["name"] = 'Combat',
        ["value"] = "• Melee: " .. checkmelee() .. "\n" ..
                    "• Sword: " .. checkweapon() .. "\n" ..
                    "• Gun: " .. checkgun(),
        ["inline"] = false
    }

    local statusField = {
        ["name"] = 'Status',
        ["value"] = "• Lever: " .. checkgatcan2() .. "\n" ..
                    "• Awaken: " .. getawaken(),
        ["inline"] = false
    }

    local data = {
        ["embeds"] = {
            {
                ["title"] = "JG - BF Check",
                ["type"] = "rich",
                ["color"] = tonumber(0x58b9ff),
                ["fields"] = {
                    playerStatsField,
                    inventoryField,
                    combatField,
                    statusField
                }
            }
        }
    }
    
    local newdata = HttpService:JSONEncode(data)
    requestt({Url = getgenv().Webhook, Body = newdata, Method = "POST", Headers = headers})
end
while wait(getgenv().Time) do
    Webhook()
end