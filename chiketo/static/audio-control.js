document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('toggleButton');
    const idolAudio = document.getElementById('idolAudio');
    const SainWaBAudio = document.getElementById('SainWaBAudio');

    // Retrieve stored state from localStorage
    let isPlaying = localStorage.getItem('isPlaying') === 'true';
    let currentTrack = localStorage.getItem('currentTrack') || 'idol'; 
    let currentTime = parseFloat(localStorage.getItem('currentTime')) || 0;

    // Ensure the button shows the correct icon based on play state
    toggleButton.src = isPlaying ? "/static/music.png" : "/static/musicoff.png";

    // Function to handle audio switching
    function playAudio(audioToPlay, audioToPause) {
        audioToPause.pause();
        audioToPlay.currentTime = currentTime;
        if (isPlaying) {
            audioToPlay.play().catch(error => {
                // Prevent autoplay issues by catching the promise rejection
                console.error('Autoplay prevented by browser', error);
            });
        }
    }

   
    if (currentTrack === 'SainWaB') {
        playAudio(SainWaBAudio, idolAudio);
    } else {
        playAudio(idolAudio, SainWaBAudio);
    }

    // Toggle play/pause on button click
    toggleButton.addEventListener('click', () => {
        if (idolAudio.paused && SainWaBAudio.paused) {
            if (currentTrack === 'idol') {
                idolAudio.play();
            } else {
                SainWaBAudio.play();
            }
            toggleButton.src = "/static/music.png";
            isPlaying = true;
        } else {
            idolAudio.pause();
            SainWaBAudio.pause();
            toggleButton.src = "/static/musicoff.png";
            isPlaying = false;
        }
        localStorage.setItem('isPlaying', isPlaying);
    });

    // Save current time and song when time is updated
    function updateAudioState(audioElement, track) {
        localStorage.setItem('currentTime', audioElement.currentTime);
        localStorage.setItem('currentTrack', track);
    }

    idolAudio.addEventListener('timeupdate', () => updateAudioState(idolAudio, 'idol'));
    SainWaBAudio.addEventListener('timeupdate', () => updateAudioState(SainWaBAudio, 'SainWaB'));

    // Switch songs when one ends with faster transition
    idolAudio.addEventListener('ended', () => {
        currentTime = 0; // Reset time for the next song
        playAudio(SainWaBAudio, idolAudio); 
        localStorage.setItem('currentTrack', 'SainWaB');
    });

    SainWaBAudio.addEventListener('ended', () => {
        currentTime = 0; // Reset time for the next song
        playAudio(idolAudio, SainWaBAudio); // Instant transition to Idol
        localStorage.setItem('currentTrack', 'idol');
    });
});
