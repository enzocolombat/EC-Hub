import { state, initPosition } from "./robot.js"

const GRID_SIZE   = 30   // pixels between grid lines
const BODY_W      = 36
const BODY_H      = 44
const WHEEL_W     = 8
const WHEEL_H     = 12
const ARROW_TIP_Y = -18  // how far forward the direction arrow points

const canvas = document.getElementById("map")
const ctx    = canvas.getContext("2d")

canvas.width  = canvas.offsetWidth  || 300
canvas.height = canvas.offsetHeight || 300

initPosition(canvas.width, canvas.height)

function drawGrid() {
    ctx.strokeStyle = "#222"
    ctx.lineWidth   = 1
    for (let x = 0; x < canvas.width; x += GRID_SIZE) {
        ctx.beginPath()
        ctx.moveTo(x, 0)
        ctx.lineTo(x, canvas.height)
        ctx.stroke()
    }
    for (let y = 0; y < canvas.height; y += GRID_SIZE) {
        ctx.beginPath()
        ctx.moveTo(0, y)
        ctx.lineTo(canvas.width, y)
        ctx.stroke()
    }
}

function drawBody() {
    ctx.fillStyle = "#333"
    ctx.fillRect(-BODY_W / 2, -BODY_H / 2, BODY_W, BODY_H)
}

function drawWheels() {
    ctx.fillStyle = "#00ff88"
    // front left, front right, rear left, rear right
    ctx.fillRect(-BODY_W / 2 - WHEEL_W, -BODY_H / 2 + 4,        WHEEL_W, WHEEL_H)
    ctx.fillRect( BODY_W / 2,           -BODY_H / 2 + 4,        WHEEL_W, WHEEL_H)
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
    ctx.fillStyle = "#111"
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    drawGrid()

    ctx.save()
    ctx.translate(state.x, state.y)
    ctx.rotate(state.angle)
    drawBody()
    drawWheels()
    drawDirectionArrow()
    ctx.restore()
}

render()