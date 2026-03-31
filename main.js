const { app, BrowserWindow, ipcMain, Tray, Menu, nativeImage } = require('electron')
const HID = require('node-hid')
const path = require('path')
const { exec } = require('child_process')

// База пристроїв HATOR
const HATOR_DEVICES = [
  {
    vendorId: 14234,
    productId: 3312,
    name: 'HATOR Quasar 3WL',
    model: 'quasar-3wl',
    type: 'mouse',
    image: 'images/quasar-3wl.png',
    wireless: true,
    features: {
      dpi: { min: 200, max: 26000, levels: 5 },
      polling: [125, 250, 500, 1000],
      buttons: [
        { id: 'left', name: 'Ліва кнопка' },
        { id: 'right', name: 'Права кнопка' },
        { id: 'middle', name: 'Колесо (натиск)' },
        { id: 'back', name: 'Кнопка назад' },
        { id: 'forward', name: 'Кнопка вперед' },
        { id: 'dpi', name: 'DPI кнопка' },
      ],
      lighting: true,
      battery: true,
      profiles: 3,
    }
  },
]

// Ігрові профілі — автоперемикання
const GAME_PROFILES = [
  { process: 'csgo', game: 'CS:GO', profile: 'Профіль 1' },
  { process: 'cs2', game: 'CS2', profile: 'Профіль 1' },
  { process: 'valorant', game: 'Valorant', profile: 'Профіль 1' },
  { process: 'dota2', game: 'Dota 2', profile: 'Профіль 2' },
  { process: 'overwatch', game: 'Overwatch', profile: 'Профіль 1' },
  { process: 'fortnite', game: 'Fortnite', profile: 'Профіль 2' },
]

let mainWindow = null
let tray = null
let currentGame = null
let gameCheckInterval = null

// ---- ГОЛОВНЕ ВІКНО ----
function createMainWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    frame: false,
    titleBarStyle: 'hidden',
    show: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  })

  mainWindow.loadFile('index.html')

  mainWindow.on('close', (e) => {
    if (tray) {
      e.preventDefault()
      mainWindow.hide()
    }
  })

  setupIPC()
  setupTray()
  startGameDetection()
  startDeviceScanning()
}

// ---- IPC ----
function setupIPC() {
  ipcMain.on('window-minimize', () => mainWindow.minimize())
  ipcMain.on('window-maximize', () => {
    if (mainWindow.isMaximized()) mainWindow.unmaximize()
    else mainWindow.maximize()
  })
  ipcMain.on('window-close', () => {
    if (tray) mainWindow.hide()
    else mainWindow.close()
  })

  ipcMain.handle('scan-devices', () => {
    try {
      const devices = HID.devices()
      const hator = devices
        .filter(d => HATOR_DEVICES.some(h => h.vendorId === d.vendorId && h.productId === d.productId))
        .reduce((acc, d) => {
          const info = HATOR_DEVICES.find(h => h.vendorId === d.vendorId && h.productId === d.productId)
          if (!acc.find(a => a.model === info.model)) {
            acc.push({ ...info, path: d.path, connected: true })
          }
          return acc
        }, [])

      return { all: devices.map(d => ({
        vendorId: d.vendorId, productId: d.productId,
        manufacturer: d.manufacturer, product: d.product,
        path: d.path, usagePage: d.usagePage, interface: d.interface
      })), hator }
    } catch (err) {
      return { all: [], hator: [], error: err.message }
    }
  })

  ipcMain.handle('get-device-db', () => HATOR_DEVICES)
  ipcMain.handle('get-game-profiles', () => GAME_PROFILES)

  ipcMain.on('add-game-profile', (event, profile) => {
    GAME_PROFILES.push(profile)
  })

  ipcMain.on('remove-game-profile', (event, index) => {
    GAME_PROFILES.splice(index, 1)
  })
}

// ---- СИСТЕМНИЙ ТРЕЙ ----
function setupTray() {
  // Простий текстовий трей для Mac
  tray = new Tray(nativeImage.createEmpty())
  tray.setTitle('H')

  const updateTrayMenu = () => {
    const menu = Menu.buildFromTemplate([
      {
        label: 'HATOR Software',
        enabled: false
      },
      { type: 'separator' },
      {
        label: currentGame ? `Гра: ${currentGame}` : 'Гра не запущена',
        enabled: false
      },
      { type: 'separator' },
      {
        label: 'Профіль 1',
        type: 'radio',
        checked: true,
        click: () => {
          if (mainWindow) mainWindow.webContents.send('switch-profile', 0)
        }
      },
      {
        label: 'Профіль 2',
        type: 'radio',
        checked: false,
        click: () => {
          if (mainWindow) mainWindow.webContents.send('switch-profile', 1)
        }
      },
      {
        label: 'Профіль 3',
        type: 'radio',
        checked: false,
        click: () => {
          if (mainWindow) mainWindow.webContents.send('switch-profile', 2)
        }
      },
      { type: 'separator' },
      {
        label: 'Відкрити',
        click: () => {
          mainWindow.show()
          mainWindow.focus()
        }
      },
      {
        label: 'Вийти',
        click: () => {
          tray.destroy()
          app.quit()
        }
      }
    ])
    tray.setContextMenu(menu)
  }

  updateTrayMenu()

  tray.on('click', () => {
    if (mainWindow.isVisible()) {
      mainWindow.hide()
    } else {
      mainWindow.show()
      mainWindow.focus()
    }
  })
}

// ---- АВТОПЕРЕМИКАННЯ ПРОФІЛІВ ----
function getRunningProcesses(callback) {
  exec('ps aux', (err, stdout) => {
    if (err) { callback([]); return }
    const processes = stdout.toLowerCase()
    callback(processes)
  })
}

function startGameDetection() {
  gameCheckInterval = setInterval(() => {
    getRunningProcesses((processes) => {
      let detectedGame = null

      for (const gp of GAME_PROFILES) {
        if (processes.includes(gp.process.toLowerCase())) {
          detectedGame = gp
          break
        }
      }

      if (detectedGame && currentGame !== detectedGame.game) {
        currentGame = detectedGame.game
        console.log(`[HATOR] Гра запущена: ${currentGame}`)
        if (mainWindow && !mainWindow.isDestroyed()) {
          mainWindow.webContents.send('game-detected', {
            game: detectedGame.game,
            profile: detectedGame.profile
          })
        }
        setupTray() // оновлюємо трей
      } else if (!detectedGame && currentGame) {
        currentGame = null
        console.log('[HATOR] Гра закрита')
        if (mainWindow && !mainWindow.isDestroyed()) {
          mainWindow.webContents.send('game-closed', {})
        }
        setupTray()
      }
    })
  }, 5000)
}

// ---- АВТОСКАНУВАННЯ ДЕВАЙСІВ ----
function startDeviceScanning() {
  let connectedModels = new Set()

  setInterval(() => {
    try {
      const devices = HID.devices()
      const hator = devices
        .filter(d => HATOR_DEVICES.some(h => h.vendorId === d.vendorId && h.productId === d.productId))
        .reduce((acc, d) => {
          const info = HATOR_DEVICES.find(h => h.vendorId === d.vendorId && h.productId === d.productId)
          if (!acc.find(a => a.model === info.model)) {
            acc.push({ ...info, path: d.path, connected: true })
          }
          return acc
        }, [])

      const currentModels = new Set(hator.map(d => d.model))
      const changed = currentModels.size !== connectedModels.size ||
        [...currentModels].some(m => !connectedModels.has(m)) ||
        [...connectedModels].some(m => !currentModels.has(m))

      if (changed) {
        connectedModels = currentModels
        if (mainWindow && !mainWindow.isDestroyed()) {
          mainWindow.webContents.send('devices-changed', { hator })
        }
      }
    } catch (err) {}
  }, 2000)
}

// ---- СТАРТ ----
app.whenReady().then(createMainWindow)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
})

app.on('activate', () => {
  if (mainWindow) {
    mainWindow.show()
    mainWindow.focus()
  }
})

app.on('before-quit', () => {
  if (gameCheckInterval) clearInterval(gameCheckInterval)
  if (tray) tray.destroy()
})