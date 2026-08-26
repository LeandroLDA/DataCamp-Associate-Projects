SELECT Product_ID, Tool_wear_min, Torque_Nm 
FROM telemetria_sensores
WHERE telemetria_sensores.OSF = 1 
ORDER BY Tool_wear_min DESC
LIMIT 5;