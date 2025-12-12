-- Mensaje de bienvenida
DEFAULT_CHAT_FRAME:AddMessage("WoW RGB cargado correctamente", 1, 1, 1)

local f = CreateFrame("Frame", "HPBeacon", UIParent)
-- Tamaño
f:SetWidth(3)
f:SetHeight(3)
-- Posicion
f:SetPoint("TOPLEFT",0,0)
-- Fondo
f:SetBackdrop({bgFile = "Interface\\Buttons\\WHITE8x8"})
f:SetBackdropColor(1, 1, 1, 1) -- Blanco al inicio
-- queda fijo
f:SetMovable(false)
f:EnableMouse(false)
-- capa "TOOLTIP" asegura que este encima de todo
f:SetFrameStrata("TOOLTIP")

-- Eventos
f:RegisterEvent("UNIT_HEALTH")
f:RegisterEvent("PLAYER_ENTERING_WORLD")

f:SetScript("OnEvent", function()
    local hp = UnitHealth("player")
    local max = UnitHealthMax("player")

    if max == 0 then max = 1 end
    local percent = hp / max

    -- Update color (escala de Grises)
    f:SetBackdropColor(percent, percent, percent, 1)
end)