We came up with 5 different possible steering/work states of the station:
```
{
    "AU": "Automatic",      # station is performing a scenario
    "RM": "Remote Manual",  # station is being steered manually from remote control panel
    "LM": "Local Manual",   # station has it's Local Manual Switch ON, and can be steered only locally
    "ID": "Idle",           # station finished performing a scenario, and is now waiting for commands
    "OF": "OFF"             # station is disabled (e.g. power switch for pumps and valves is OFF)
}
```

As the state can be always overwritten locally (with the physical switches),
we figured out, that the state should be stored locally, on the station driver.
Station state should be included in every heartbeat update request, so the backend is aware of any changes.

Steering state can be changed by the user in the following ways:
1. No matter what, if the Local Manual Switch is enabled, the state is always LM (and gets changed to LM if needed).
2. To enable Remote Manual state, backend hits an endpoint `/manual`, and this request should always succeed,
unless the state is LM or OF.
3. The station can go into AU state from RM and ID states. To conduct that, backend hits an endpoint `/automatic`,
which also retrieves a scenario.
4. The station should switch into ID (Idle) state each time a scenario finishes, the Local Manual Switch is being
turned OFF, or the station is being powered on (is coming up from the OF state) – this should happen automatically,
without any signal from the backend.
5. Every state change should trigger heartbeat update request to the backend.