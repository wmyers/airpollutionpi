## Adding power button(s)

It is not a good idea to just yank out the usb power plug on the `pi-in-a-bottle` as this can potentially affect the sd card. Before detaching any cables you need to power down the pi with the following command:

```
sudo halt
```

See more info here: <https://howchoo.com/g/zmexnjbhmjb/dont-pull-the-plug-how-to-shut-down-or-restart-your-raspberry-pi-properly>

We are going to go one step further and add a **momentary push button** to tell the pi to power down (so we don't have to `ssh` into it and power it down with a command).

These push buttons can be purchased very cheaply here:

![](https://cdn.shopify.com/s/files/1/0176/3274/products/1503-06_1024x1024.jpg?v=1546149378)
<https://thepihut.com/products/adafruit-16mm-panel-mount-momentary-pushbutton-burgundy>

We need to solder this button onto the pi-zero using two jumper cables. We need to solder one cable onto one of the `GPIO` pin holes on the pi and the other cable onto one of the `Ground` pin holes. 

![](https://i0.wp.com/opensourceforu.com/wp-content/uploads/2017/06/Figure-1-Raspberry-Pi-pinout-diagram.jpg)

When we press the button a connection will be made and the pi will power down.

But what about powering up again? Well if we can use pin 5 (`GPIO 3`), aka the _only dedicated power up/down pinhole of the pi_, then we could both power-down and power-up by pushing the same button. 

We could then also add a script to power-up/down according to the length of time the button is held etc, see here: <https://howchoo.com/g/mwnlytk3zmm/how-to-add-a-power-button-to-your-raspberry-pi>

However the `pi-in-a-bottle` is already using `GPIO 3` for the humidity sensor. So we need to use a different `GPIO`. The good news is that we can use any other `GPIO` for powering down the pi, but can apparently only use pin 5 (`GPIO 3`) for both power-up _and_ power-down.

Nevermind let's use pin 37 (`GPIO 26`) to power-down and we can attach a usb switch to sit between the pi and the power-pack to turn the pi back on again after it has been powered down.

These usb switches can be purchased very cheaply here:

![](https://cdn.shopify.com/s/files/1/0176/3274/products/100290_1024x1024.jpg?v=1542644765)
<https://thepihut.com/products/usb-cable-with-switch>


So to summarise we need to do the following:

1. solder one end of a jumper lead onto pin 37 (`GPIO 26`), or another spare GPIO pinhole, and solder the other end onto one terminal of the momentary push button
2. solder one end of a jumper lead onto a Ground pinhole, e.g. pin 39, and solder the other end onto the other terminal of the push button
3. attach the usb switch onto the cable between the pi and the power-pack, so that it can be switched off _**after**_ the pi has powered down, and switched on again to power the pi back up.

### The last bit

We need to tell the pi that a different pinhole is being used to power down the pi. This is surprisingly easy, just add the following line of code to `/boot/config.txt`:

```
dtoverlay=gpio-shutdown,gpio_pin=26
```

You can read a bit more on that here:
<https://www.raspberrypi.org/forums/viewtopic.php?t=217442>
