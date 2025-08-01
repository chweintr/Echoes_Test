# How to Remove Reverb Completely

If the reverb is still too much, here's how to remove it entirely:

## Option 1: Quick Disable (Recommended)
In `oracle_interface_styled.html`, find this section around line 460:

```javascript
// Connect to reverb
const source = this.audioContext.createMediaElementSource(audio);
source.connect(this.reverbNode);
this.reverbNode.connect(this.audioContext.destination);
```

Replace with:
```javascript
// Direct connection (no reverb)
const source = this.audioContext.createMediaElementSource(audio);
source.connect(this.audioContext.destination);
```

## Option 2: Disable Reverb Setup
Find the line around 443:
```javascript
if (!this.audioContext) {
    this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
    this.setupReverb();
}
```

Replace with:
```javascript
if (!this.audioContext) {
    this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
    // Reverb disabled
}
```

## Option 3: Return to Simple Audio
Replace the entire `playNextAudio()` function with:
```javascript
async playNextAudio() {
    if (this.audioQueue.length === 0) {
        this.isPlaying = false;
        return;
    }
    
    this.isPlaying = true;
    const audioData = this.audioQueue.shift();
    
    try {
        const audio = new Audio(`data:audio/mp3;base64,${audioData}`);
        
        // Set volume
        if (this.currentPersona === 'kurt-vonnegut') {
            audio.volume = 1.0; // Max volume for Vonnegut
        } else {
            audio.volume = 0.9; // Slightly higher volume for Oracle
        }
        
        audio.onended = () => {
            this.playNextAudio();
        };
        
        await audio.play();
    } catch (e) {
        console.error('Audio play failed:', e);
        this.playNextAudio();
    }
}
```

This removes all Web Audio API complexity and returns to simple audio playback.