const HID = require('./node_modules/node-hid')
const devices = HID.devices().filter(d => d.vendorId === 14234 && d.productId === 3312 && d.usagePage === 65285)

if (!devices.length) {
  console.log('Не знайдено')
  process.exit()
}

console.log('Підключаємось до:', devices[0].path)

try {
  const d = new HID.HID(devices[0].path)
  d.on('data', data => {
    console.log('Пакет:', Array.from(data).map(b => b.toString(16).padStart(2,'0')).join(' '))
  })
  d.on('error', e => console.log('Помилка:', e.message))
  console.log('Слухаємо 10 секунд, ворухни мишкою...')
  setTimeout(() => { try { d.close() } catch(e) {} process.exit() }, 10000)
} catch(e) {
  console.log('Помилка підключення:', e.message)
}

