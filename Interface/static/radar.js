import { state } from "./robot.js"
import { render } from "./canvas.js"

const MAX_DISTANCE_CM = 150  // obstacles beyond this are ignored
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
        if (distance > MAX_DISTANCE_CM || distance < 2) return
        document.getElementById("dstc").textContent = distance + " cm"
        // Rotate scan angle by robot heading so obstacles are plotted
        // in world space, not robot space
        const rad = (angle * (Math.PI / 180)) + state.angle - (Math.PI / 2)

        const x = state.x + Math.sin(rad) * distance * SCALE_PX_PER_CM
        const y = state.y - Math.cos(rad) * distance * SCALE_PX_PER_CM

        obstacles.push({ x, y, angle })
        renderObstacles(ctx)
})
}


export function renderObstacles(ctx) {
    if (obstacles.length < 2) return

    // Split obstacles into forward and backward sweeps
    // Forward sweep = angle increasing, backward = angle decreasing
    const sweeps = []
    let current  = [obstacles[0]]

    for (let i = 1; i < obstacles.length; i++) {
        const prev = obstacles[i - 1]
        const curr = obstacles[i]

        // Direction changed — start a new sweep
        if ((curr.angle - prev.angle) * (prev.angle - (obstacles[i - 2]?.angle ?? prev.angle)) < 0) {
            sweeps.push(current)
            current = [curr]
        } else {
            current.push(curr)
        }
    }
    sweeps.push(current)

    // Draw each sweep independently
    for (const sweep of sweeps) {
        if (sweep.length < 2) continue

        ctx.strokeStyle = "#ff4444"
        ctx.lineWidth   = 1.5
        ctx.beginPath()
        ctx.moveTo(sweep[0].x, sweep[0].y)
        for (const { x, y } of sweep.slice(1)) {
            ctx.lineTo(x, y)
        }
        ctx.stroke()
    }

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