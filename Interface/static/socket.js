import { applyGyro, applyMove, applyRotation } from "./robot.js"
import { render } from "./canvas.js"
import { initRadar } from "./radar.js"   
const DEFAULT_SPEED = 60
const MOVE_TICK_MS  = 50  // interval between position updates while key is held

const socket = io()

// --- Connection status ---

socket.on("connect", () => {
    setStatus("Connected", "online")
})

socket.on("disconnect", () => {
    setStatus("Disconnected", "offline")
})

const canvas = document.getElementById("map")
const ctx    = canvas.getContext("2d")
initRadar(socket, canvas, ctx)

function setStatus(label, cssClass) {
    const el = document.getElementById("status")
    el.textContent  = label
    el.className    = cssClass
}

// --- Gyroscope stream ---

socket.on("gyro", (data) => {
    if (!data?.gyro) return

    updateGyroDisplay(data.gyro, data.temp)
    applyGyro(data.gyro.z)
    render()
})
socket.on("scan_point", (point) => {
        if (distance > MAX_DISTANCE_CM) return
        const { angle, distance } = point
        document.getElementById("dstc").textContent = distance + " cm"
        console.log(distance)

})

function updateGyroDisplay(gyro, temp) {
    document.getElementById("gx").textContent   = gyro.x.toFixed(2)
    document.getElementById("gy").textContent   = gyro.y.toFixed(2)
    document.getElementById("gz").textContent   = gyro.z.toFixed(2)
    document.getElementById("temp").textContent = temp
}


// --- Keyboard input ---

const KEY_ACTION_MAP = {
    ArrowUp:    "forward",
    ArrowDown:  "backward",
    ArrowLeft:  "left",
    ArrowRight: "right",
    " ":        "stop",
}

let activeInterval = null

document.addEventListener("keydown", (e) => {
    const action = KEY_ACTION_MAP[e.key]
    if (!action || activeInterval) return

    document.getElementById(`btn-${action}`)?.classList.add("active")
    socket.emit("command", { action, speed: DEFAULT_SPEED })

    activeInterval = setInterval(() => {
        if (action === "forward"  || action === "backward") applyMove(action)
        if (action === "left"     || action === "right")    applyRotation(action)
        render()
    }, MOVE_TICK_MS)
})

document.addEventListener("keyup", (e) => {
    const action = KEY_ACTION_MAP[e.key]
    if (!action) return

    document.getElementById(`btn-${action}`)?.classList.remove("active")
    socket.emit("command", { action: "stop", speed: 0 })

    clearInterval(activeInterval)
    activeInterval = null
})