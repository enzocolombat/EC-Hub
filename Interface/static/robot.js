const MOVE_SPEED_PX    = 3      // pixels per tick at nominal speed
const ROTATION_STEP    = 0.05   // radians per tick (keyboard turn)
const GYRO_SAMPLE_DT   = 0.05   // seconds between gyro samples (20 Hz)
const DEG_TO_RAD       = Math.PI / 180

export const state = {
    x:     null,  // set after canvas init
    y:     null,
    angle: 0,     // radians, 0 = pointing up
}

export function initPosition(canvasWidth, canvasHeight) {
    state.x = canvasWidth  / 2
    state.y = canvasHeight / 2
}

// Integrate gyroscope Z angular velocity into heading
export function applyGyro(gz) {
    if (typeof gz !== "number" || !isFinite(gz)) return
    state.angle += gz * GYRO_SAMPLE_DT * DEG_TO_RAD
}

// Advance or retreat along current heading
export function applyMove(direction) {
    const sign = direction === "forward" ? 1 : -1
    state.x += Math.sin(state.angle) * MOVE_SPEED_PX * sign
    state.y -= Math.cos(state.angle) * MOVE_SPEED_PX * sign
}

// Rotate in place (keyboard fallback, before real encoders arrive)
export function applyRotation(direction) {
    state.angle += direction === "right" ? ROTATION_STEP : -ROTATION_STEP
}