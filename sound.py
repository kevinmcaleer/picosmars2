import machine
import time
import math
import random

# Define the PWM pin
pwm = machine.PWM(machine.Pin(0))

PWM_FREQ = 44100
pwm.freq(PWM_FREQ)  # Set the PWM frequency

def play_sound_effect(waveShape, startFrequency, endFrequency, startVolume, endVolume, duration, effect, interpolation):
    num_samples = int(PWM_FREQ * duration / 1000)

    for i in range(num_samples):
        t = i / PWM_FREQ
        factor = i / num_samples
        
        # Interpolation
        if interpolation == 'linear':
            freq = startFrequency + factor * (endFrequency - startFrequency)
        elif interpolation == 'curve':
            freq = startFrequency + (endFrequency - startFrequency) * math.sqrt(factor)
        else:  # 'logarithmic'
            freq = startFrequency + (endFrequency - startFrequency) * (math.log(factor * 10 + 1) / math.log(10.1))
        
        # Wave generation
        if waveShape == 'sine':
            y = math.sin(2 * math.pi * freq * t)
        elif waveShape == 'sawtooth':
            y = 2 * (t * freq - math.floor(t * freq + 0.5))
        elif waveShape == 'triangle':
            y = 2 * abs(2 * (t * freq - math.floor(t * freq + 0.5))) - 1
        elif waveShape == 'square':
            y = 1 - 2 * math.floor(2 * t * freq)
        else:  # 'noise'
            y = 2 * (random.random() - 0.5)

        # Volume and effect
        volume = startVolume + factor * (endVolume - startVolume)
        
        if effect == 'tremolo':
            y *= (1 + 0.1 * math.sin(2 * math.pi * 6 * t))
        elif effect == 'vibrato':
            y *= math.sin(2 * math.pi * (freq + 5 * math.sin(2 * math.pi * 6 * t)) * t)
        elif effect == 'warble':
            y *= math.sin(2 * math.pi * (freq + 10 * math.sin(2 * math.pi * 20 * t)) * t)
        
        y *= volume
        sample = int((y + 1) / 2 * 65535)

        # Play sound using PWM
        pwm.duty_u16(sample)
        time.sleep(1/PWM_FREQ)

# Test
# play_sound_effect('square', 1600, 1, 255, 0, 300, 'none', 'curve')

play_sound_effect('noise',
        54,
        54,
        255,
        0,
        500,
        'none',
        'linear')

