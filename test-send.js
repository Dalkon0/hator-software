const HID = require('./node_modules/node-hid')
const devices = HID.devices().filter(d => d.vendorId === 14234 && d.productId === 3312)

console.log('Всі інтерфейси:')
devices.forEach((d, i) => console.log(i, 'usagePage:', d.usagePage, 'interface:', d.interface, 'path:', d.path))

// Спробуємо підключитись до кожного і відправити запит статусу
devices.forEach((dev, i) => {
  try {
    const d = new HID.HID(dev.path)
    
    // Стандартний запит статусу батареї (0x01) і заряду
    try {
      d.write([0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
      const data = d.readSync()
      if (data && data.length > 0) {
        console.log(`Interface ${i} відповів:`, Array.from(data).map(b => b.toString(16).padStart(2,'0')).join(' '))
      }
    } catch(e) {}
    
    d.close()
  } catch(e) {
    console.log(`Interface ${i}: помилка -`, e.message)
  }
})
