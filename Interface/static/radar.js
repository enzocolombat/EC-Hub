import { state } from "./robot.js"
import { render } from "./canvas.js"

const MAX_DISTANCE_CM = 200  // obstacles beyond this are ignored
const SCALE_PX_PER_CM = 2.57  // canvas pixels per cm

let obstacles = []  // cleared on each new scan


export function initRadar(socket, canvas, ctx) {
    const btn = document.getElementById("btn-scan")
    document.getElementById("btn-clear").addEventListener("click", () => {
    clearObstacles()
    renderObstacles(ctx)
})
    btn.addEventListener("click", () => {
        socket.emit("start_scan")
    })

    socket.on("scan_status", (data) => {
      if (data.status === "started") {
          btn.disabled    = true
          btn.textContent = "Scanning..."
       }
      if (data.status === "complete") {
          btn.disabled    = false
          btn.textContent = "Scan"
      }
      if (data.status === "busy") {
        console.warn("Scan already in progress")
      }
})

    socket.on("scan_point", (point) => {
        const { angle, distance } = point
        if (distance > MAX_DISTANCE_CM) return
        document.getElementById("dstc").textContent = distance + " cm"
        // Rotate scan angle by robot heading so obstacles are plotted
        // in world space, not robot space
        const rad = (angle * (Math.PI / 180)) + state.angle - (Math.PI / 2)

        const x = state.x + Math.sin(rad) * distance * SCALE_PX_PER_CM
        const y = state.y - Math.cos(rad) * distance * SCALE_PX_PER_CM

        obstacles.push({ x, y })
        renderObstacles(ctx)
})
}


export function renderObstacles(ctx) {
    if (obstacles.length < 2) return

    // Draw connecting line
    ctx.strokeStyle = "#ff4444"
    ctx.lineWidth   = 1.5
    ctx.beginPath()
    ctx.moveTo(obstacles[0].x, obstacles[0].y)
    for (const { x, y } of obstacles.slice(1)) {
        ctx.lineTo(x, y)
    }
    ctx.stroke()

    // Draw points on top
    ctx.fillStyle = "#ff4444"
    for (const { x, y } of obstacles) {
        ctx.beginPath()
        ctx.arc(x, y, 3, 0, Math.PI * 2)
        ctx.fill()
    }
}
export function clearObstacles() {
    obstacles = []
}