const socket = new WebSocket('ws://127.0.0.1:8001/');

let context = new AudioContext(),
    sound = new Audio('sounds/nothing_detected.mp3'),
    source = context.createMediaElementSource(sound),
    gain = context.createGain(),
    stereoPanner = context.createStereoPanner(),
    filter = context.createBiquadFilter(),
    compressor = context.createDynamicsCompressor(),
    isPlaying = false,
    playStopButton = document.querySelector('#playStopButton');

let filterSliders = document.getElementsByClassName('filterSlider');
let filterSelectList = document.querySelector('#filterSelectList');
let compressorSliders = document.getElementsByClassName('compressorSlider');

source.connect(gain);
gain.connect(stereoPanner);
stereoPanner.connect(filter);
filter.connect(compressor);
compressor.connect(context.destination);

document.querySelector('#gainSlider').addEventListener('input', function (e) {
    let gainValue = (this.value / 10);
    document.querySelector('#gainOutput').innerHTML = gainValue + ' dB';
    gain.gain.value = gainValue;
});

document.querySelector('#panningSlider').addEventListener('input', function (e) {
    let panValue = (this.value - 50) / 50;
    document.querySelector('#panningOutput').innerHTML = panValue + ' LR';
    stereoPanner.pan.value = panValue;
});


for (let i = 0; i < filterSliders.length; i++) {
    filterSliders[i].addEventListener('mousemove', changeFilterParameter, false);
}

filterSelectList.addEventListener('change', function (e) {
    filter.type = filterSelectList.options[filterSelectList.selectedIndex].value;
});

function changeFilterParameter() {
    switch (this.id) {
    case 'frequencySlider':
        filter.frequency.value = (this.value);
        document.querySelector('#frequencyOutput').innerHTML = (this.value) + ' Hz';
        break;
    case 'detuneSlider':
        filter.detune.value = (this.value);
        document.querySelector('#detuneOutput').innerHTML = (this.value) + ' cents';
        break;
    case 'qSlider':
        filter.Q.value = (this.value);
        document.querySelector('#qOutput').innerHTML = (this.value) + ' ';
        break;
    case 'gainSlider':
        filter.gain.value = (this.value);
        document.querySelector('#gainOutput').innerHTML = (this.value) + ' dB';
        break;
    }
};

for (let i = 0; i < compressorSliders.length; i++) {
    compressorSliders[i].addEventListener('mousemove', changeCompressorParameter);
}

function changeCompressorParameter() {
    switch(this.id) {
        case 'thresholdSlider':
            compressor.threshold.value = (this.value - 100);
            document.querySelector('#thresholdOutput').innerHTML = (this.value - 100) + ' dB';
            break;
        case 'ratioSlider':
            compressor.ratio.value = (this.value / 5);
            document.querySelector('#ratioOutput').innerHTML = (this.value / 5) + ' dB';
            break;
        case 'kneeSlider':
            compressor.knee.value = (this.value / 2.5);
            document.querySelector('#kneeOutput').innerHTML = (this.value / 2.5) + ' degree';
            break;
        case 'attackSlider':
            compressor.attack.value = (this.value / 1000);
            document.querySelector('#attackOutput').innerHTML = (this.value / 1000) + ' sec';
            break;
        case 'releaseSlider':
            compressor.release.value = (this.value / 1000);
            document.querySelector('#releaseOutput').innerHTML = (this.value / 1000) + ' sec';
            break;
    }
};

playStopButton.addEventListener('click', function (e) {
    if (isPlaying) {
        sound.pause();
        playStopButton.innerHTML = 'Play';
    } else {
        sound.play();
        playStopButton.innerHTML = 'Stop';
    }
    isPlaying = !isPlaying;
});

sound.addEventListener('ended', function (e) {
    isPlaying = false;
    playStopButton.innerHTML = 'Play';
});

function receiveAudio(socket) {
    socket.addEventListener('message', ({ data }) => {
        const event = JSON.parse(data);
  
        if(event.type == 'detected') {
            sound = new Audio('sounds/' + event.fruit + '.mp3');
            source = context.createMediaElementSource(sound),

            source.connect(gain);
            gain.connect(stereoPanner);
            stereoPanner.connect(filter);
            filter.connect(compressor);
            compressor.connect(context.destination);

            if (isPlaying) {
                sound.pause();
            } else {
                sound.play();
            }

            sound.addEventListener('ended', function (e) {
                isPlaying = false;
                playStopButton.innerHTML = 'Play';
            });

        } else {
            console.log('Unsupported event type');
        }
    });
};

receiveAudio(socket);
