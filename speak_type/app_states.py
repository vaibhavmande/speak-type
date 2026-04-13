class AppStates:
    IDLE = "IDLE"
    RECORDING = "RECORDING"
    PROCESSING = "PROCESSING"


def get_app_metadata(state, app_config):
    match state:
        case AppStates.IDLE:
            title = app_config.get("idle_icon")
        case AppStates.RECORDING:
            title = app_config.get("recording_icon")
        case AppStates.PROCESSING:
            title = app_config.get("processing_icon")
        case _:
            title = app_config.get("idle_icon")

    return {"title": title}
