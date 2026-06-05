import { state, initPosition } from "./robot.js"
import { renderObstacles } from "./radar.js"

const GRID_SIZE   = 30
const BODY_W      = 36
const BODY_H      = 44
const WHEEL_W     = 8
const WHEEL_H     = 12
const ARROW_TIP_Y = -18

const ZOOM_STEP = 0.1
const ZOOM_MIN  = 0.2
const ZOOM_MAX  = 5.0

export const canvas = document.getElementById("map")
export const ctx    = canvas.getContext("2d")

canvas.width  = canvas.offsetWidth  || 300
canvas.height = canvas.offsetHeight || 300

initPosition(canvas.width, canvas.height)

const viewport = {
    offsetX: 0,
    offsetY: 0,
    follow:  true,
    zoom:    1.0,
}

// Switch between follow and free mode
document.getElementById("btn-follow").addEventListener("click", () => {
    viewport.follow = !viewport.follow
    document.getElementById("btn-follow").textContent =
        viewport.follow ? "Free cam" : "Follow"
})

// --- Mouse drag (free mode only) ---
let drag = { active: false, startX: 0, startY: 0, originX: 0, originY: 0 }

canvas.addEventListener("mousedown", (e) => {
    if (viewport.follow) return
    drag = {
        active:  true,
        startX:  e.clientX,
        startY:  e.clientY,
        originX: viewport.offsetX,
        originY: viewport.offsetY,
    }
})

canvas.addEventListener("mousemove", (e) => {
    if (!drag.active) return
    viewport.offsetX = drag.originX + (e.clientX - drag.startX)
    viewport.offsetY = drag.originY + (e.clientY - drag.startY)
    render()
})

canvas.addEventListener("mouseup",   () => { drag.active = false })
canvas.addEventListener("mouseleave", () => { drag.active = false })

canvas.addEventListener("wheel", (e) => {
    e.preventDefault()

    const delta   = e.deltaY > 0 ? -ZOOM_STEP : ZOOM_STEP
    const newZoom = Math.min(ZOOM_MAX, Math.max(ZOOM_MIN, viewport.zoom + delta))

    const mouseX = e.offsetX
    const mouseY = e.offsetY
    const { tx, ty } = getTransform()

    viewport.offsetX -= mouseX / viewport.zoom * (newZoom - viewport.zoom)
    viewport.offsetY -= mouseY / viewport.zoom * (newZoom - viewport.zoom)
    viewport.zoom     = newZoom

    render()
}, { passive: false })


function getTransform() {
    const tx = viewport.follow
        ? canvas.width  / 2 - state.x * viewport.zoom
        : viewport.offsetX

    const ty = viewport.follow
        ? canvas.height / 2 - state.y * viewport.zoom
        : viewport.offsetY

    return { tx, ty }
}

function drawGrid(tx, ty) {
    ctx.strokeStyle = "#222"
    ctx.lineWidth   = 1

    const startX = ((tx % GRID_SIZE) + GRID_SIZE) % GRID_SIZE
    const startY = ((ty % GRID_SIZE) + GRID_SIZE) % GRID_SIZE

    for (let x = startX; x < canvas.width;  x += GRID_SIZE) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke()
    }
    for (let y = startY; y < canvas.height; y += GRID_SIZE) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke()
    }
}

function drawBody() {
    ctx.fillStyle = "#333"
    ctx.fillRect(-BODY_W / 2, -BODY_H / 2, BODY_W, BODY_H)
}

function drawWheels() {
    ctx.fillStyle = "#00ff88"
    ctx.fillRect(-BODY_W / 2 - WHEEL_W, -BODY_H / 2 + 4,            WHEEL_W, WHEEL_H)
    ctx.fillRect( BODY_W / 2,           -BODY_H / 2 + 4,            WHEEL_W, WHEEL_H)
    ctx.fillRect(-BODY_W / 2 - WHEEL_W,  BODY_H / 2 - 4 - WHEEL_H, WHEEL_W, WHEEL_H)
    ctx.fillRect( BODY_W / 2,            BODY_H / 2 - 4 - WHEEL_H, WHEEL_W, WHEEL_H)
}

function drawDirectionArrow() {
    ctx.fillStyle = "#ffffff"
    ctx.beginPath()
    ctx.moveTo(0,  ARROW_TIP_Y)
    ctx.lineTo(7,  ARROW_TIP_Y + 10)
    ctx.lineTo(-7, ARROW_TIP_Y + 10)
    ctx.closePath()
    ctx.fill()
}

export function render() {
    const { tx, ty } = getTransform()

    ctx.fillStyle = "#111"
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    drawGrid(tx, ty)

    ctx.save()
    ctx.translate(tx, ty)
    ctx.scale(viewport.zoom, viewport.zoom)
    renderObstacles(ctx)
    ctx.restore()

    ctx.save()
    ctx.translate(state.x * viewport.zoom + tx, state.y * viewport.zoom + ty)
    ctx.rotate(state.angle)
    ctx.scale(viewport.zoom, viewport.zoom)
    drawBody()
    drawWheels()
    drawDirectionArrow()
    ctx.restore()
}

render()