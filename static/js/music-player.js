// Music Player JavaScript
class MusicPlayer {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.audio = null;
        this.currentTrack = 0;
        this.isPlaying = false;
        this.playlist = [];
        this.volume = 0.7;
        
        this.init();
    }
    
    init() {
        this.createPlayerHTML();
        this.bindEvents();
    }
    
    createPlayerHTML() {
        this.container.innerHTML = `
            <div class="music-player">
                <div class="music-player-content">
                    <!-- Informações da música -->
                    <div class="music-info">
                        <h3 class="music-title" id="musicTitle">Selecione uma música</h3>
                        <p class="music-artist" id="musicArtist">Artista</p>
                        <p class="music-album" id="musicAlbum">Álbum</p>
                    </div>
                    
                    <!-- Visualizador (opcional) -->
                    <div class="music-visualizer" id="musicVisualizer" style="display: none;">
                        <div class="visualizer-bar"></div>
                        <div class="visualizer-bar"></div>
                        <div class="visualizer-bar"></div>
                        <div class="visualizer-bar"></div>
                        <div class="visualizer-bar"></div>
                        <div class="visualizer-bar"></div>
                        <div class="visualizer-bar"></div>
                    </div>
                    
                    <!-- Controles principais -->
                    <div class="music-controls">
                        <button class="control-btn small" id="prevBtn">
                            <i data-feather="skip-back"></i>
                        </button>
                        <button class="control-btn large" id="playPauseBtn">
                            <i data-feather="play" id="playIcon"></i>
                        </button>
                        <button class="control-btn small" id="nextBtn">
                            <i data-feather="skip-forward"></i>
                        </button>
                    </div>
                    
                    <!-- Barra de progresso -->
                    <div class="progress-container">
                        <div class="progress-info">
                            <span id="currentTime">0:00</span>
                            <span id="totalTime">0:00</span>
                        </div>
                        <div class="progress-bar" id="progressBar">
                            <div class="progress-fill" id="progressFill"></div>
                        </div>
                    </div>
                    
                    <!-- Controle de volume -->
                    <div class="volume-control">
                        <button class="volume-btn" id="volumeBtn">
                            <i data-feather="volume-2" id="volumeIcon"></i>
                        </button>
                        <div class="volume-slider" id="volumeSlider">
                            <div class="volume-fill" id="volumeFill"></div>
                        </div>
                    </div>
                    
                    <!-- Playlist -->
                    <div class="playlist-section" id="playlistSection" style="display: none;">
                        <h4 class="playlist-title">Playlist</h4>
                        <div id="playlistItems"></div>
                    </div>
                </div>
            </div>
        `;
        
        // Inicializar ícones do Feather
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
    }
    
    bindEvents() {
        // Botão play/pause
        document.getElementById('playPauseBtn').addEventListener('click', () => {
            this.togglePlayPause();
        });
        
        // Botões de navegação
        document.getElementById('prevBtn').addEventListener('click', () => {
            this.previousTrack();
        });
        
        document.getElementById('nextBtn').addEventListener('click', () => {
            this.nextTrack();
        });
        
        // Barra de progresso
        document.getElementById('progressBar').addEventListener('click', (e) => {
            this.seekTo(e);
        });
        
        // Controle de volume
        document.getElementById('volumeBtn').addEventListener('click', () => {
            this.toggleMute();
        });
        
        document.getElementById('volumeSlider').addEventListener('click', (e) => {
            this.changeVolume(e);
        });
        
        // Atalhos do teclado
        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space' && e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
                e.preventDefault();
                this.togglePlayPause();
            }
        });
    }
    
    loadPlaylist(playlist) {
        this.playlist = playlist;
        this.renderPlaylist();
        if (playlist.length > 0) {
            document.getElementById('playlistSection').style.display = 'block';
        }
    }
    
    renderPlaylist() {
        const container = document.getElementById('playlistItems');
        container.innerHTML = '';
        
        this.playlist.forEach((track, index) => {
            const item = document.createElement('div');
            item.className = `playlist-item ${index === this.currentTrack ? 'active' : ''}`;
            item.innerHTML = `
                <div class="playlist-item-info">
                    <div class="playlist-item-title">${track.title}</div>
                    <div class="playlist-item-artist">${track.artist}</div>
                </div>
                <div class="playlist-item-duration">${track.duration || '0:00'}</div>
            `;
            
            item.addEventListener('click', () => {
                this.loadTrack(index);
            });
            
            container.appendChild(item);
        });
    }
    
    loadTrack(index) {
        if (!this.playlist[index]) return;
        
        this.currentTrack = index;
        const track = this.playlist[index];
        
        // Atualizar informações da música
        document.getElementById('musicTitle').textContent = track.title;
        document.getElementById('musicArtist').textContent = track.artist;
        document.getElementById('musicAlbum').textContent = track.album || '';
        
        // Criar novo elemento de áudio
        if (this.audio) {
            this.audio.pause();
            this.audio.removeEventListener('timeupdate', this.updateProgress);
            this.audio.removeEventListener('ended', this.trackEnded);
        }
        
        this.audio = new Audio(track.url);
        this.audio.volume = this.volume;
        
        // Eventos do áudio
        this.audio.addEventListener('loadedmetadata', () => {
            document.getElementById('totalTime').textContent = this.formatTime(this.audio.duration);
        });
        
        this.audio.addEventListener('timeupdate', () => {
            this.updateProgress();
        });
        
        this.audio.addEventListener('ended', () => {
            this.trackEnded();
        });
        
        // Atualizar playlist visual
        this.updatePlaylistUI();
        
        // Mostrar visualizador se estiver tocando
        if (this.isPlaying) {
            this.audio.play();
            document.getElementById('musicVisualizer').style.display = 'flex';
        }
    }
    
    togglePlayPause() {
        if (!this.audio) {
            if (this.playlist.length > 0) {
                this.loadTrack(0);
            } else {
                return;
            }
        }
        
        if (this.isPlaying) {
            this.pause();
        } else {
            this.play();
        }
    }
    
    play() {
        if (this.audio) {
            this.audio.play();
            this.isPlaying = true;
            document.getElementById('playIcon').setAttribute('data-feather', 'pause');
            document.getElementById('musicVisualizer').style.display = 'flex';
            if (typeof feather !== 'undefined') {
                feather.replace();
            }
        }
    }
    
    pause() {
        if (this.audio) {
            this.audio.pause();
            this.isPlaying = false;
            document.getElementById('playIcon').setAttribute('data-feather', 'play');
            document.getElementById('musicVisualizer').style.display = 'none';
            if (typeof feather !== 'undefined') {
                feather.replace();
            }
        }
    }
    
    previousTrack() {
        if (this.currentTrack > 0) {
            this.loadTrack(this.currentTrack - 1);
        } else {
            this.loadTrack(this.playlist.length - 1);
        }
    }
    
    nextTrack() {
        if (this.currentTrack < this.playlist.length - 1) {
            this.loadTrack(this.currentTrack + 1);
        } else {
            this.loadTrack(0);
        }
    }
    
    trackEnded() {
        this.nextTrack();
    }
    
    updateProgress() {
        if (!this.audio) return;
        
        const progress = (this.audio.currentTime / this.audio.duration) * 100;
        document.getElementById('progressFill').style.width = progress + '%';
        document.getElementById('currentTime').textContent = this.formatTime(this.audio.currentTime);
    }
    
    seekTo(e) {
        if (!this.audio) return;
        
        const progressBar = document.getElementById('progressBar');
        const clickX = e.offsetX;
        const width = progressBar.offsetWidth;
        const newTime = (clickX / width) * this.audio.duration;
        
        this.audio.currentTime = newTime;
    }
    
    changeVolume(e) {
        const volumeSlider = document.getElementById('volumeSlider');
        const clickX = e.offsetX;
        const width = volumeSlider.offsetWidth;
        const newVolume = clickX / width;
        
        this.volume = newVolume;
        if (this.audio) {
            this.audio.volume = this.volume;
        }
        
        document.getElementById('volumeFill').style.width = (this.volume * 100) + '%';
        this.updateVolumeIcon();
    }
    
    toggleMute() {
        if (this.audio) {
            if (this.audio.volume > 0) {
                this.previousVolume = this.audio.volume;
                this.audio.volume = 0;
                this.volume = 0;
            } else {
                this.audio.volume = this.previousVolume || 0.7;
                this.volume = this.audio.volume;
            }
            
            document.getElementById('volumeFill').style.width = (this.volume * 100) + '%';
            this.updateVolumeIcon();
        }
    }
    
    updateVolumeIcon() {
        const volumeIcon = document.getElementById('volumeIcon');
        
        if (this.volume === 0) {
            volumeIcon.setAttribute('data-feather', 'volume-x');
        } else if (this.volume < 0.5) {
            volumeIcon.setAttribute('data-feather', 'volume-1');
        } else {
            volumeIcon.setAttribute('data-feather', 'volume-2');
        }
        
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
    }
    
    updatePlaylistUI() {
        const items = document.querySelectorAll('.playlist-item');
        items.forEach((item, index) => {
            if (index === this.currentTrack) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
    }
    
    formatTime(seconds) {
        if (isNaN(seconds)) return '0:00';
        
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = Math.floor(seconds % 60);
        return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    }
    
    // Método para adicionar uma música à playlist
    addTrack(track) {
        this.playlist.push(track);
        this.renderPlaylist();
        if (this.playlist.length === 1) {
            document.getElementById('playlistSection').style.display = 'block';
        }
    }
    
    // Método para remover uma música da playlist
    removeTrack(index) {
        this.playlist.splice(index, 1);
        if (index <= this.currentTrack && this.currentTrack > 0) {
            this.currentTrack--;
        }
        this.renderPlaylist();
        if (this.playlist.length === 0) {
            document.getElementById('playlistSection').style.display = 'none';
        }
    }
}

// Inicialização automática se o container existir
document.addEventListener('DOMContentLoaded', function() {
    const musicPlayerContainer = document.getElementById('musicPlayer');
    if (musicPlayerContainer) {
        window.musicPlayer = new MusicPlayer('musicPlayer');
        
        // Exemplo de playlist (você pode substituir pelos seus dados)
        const examplePlaylist = [
            {
                title: "Música de Exemplo 1",
                artist: "Artista 1",
                album: "Álbum 1",
                url: "/media/musicas/exemplo1.mp3",
                duration: "3:45"
            },
            {
                title: "Música de Exemplo 2",
                artist: "Artista 2",
                album: "Álbum 2",
                url: "/media/musicas/exemplo2.mp3",
                duration: "4:12"
            }
        ];
        
        // Carregar playlist de exemplo (remova esta linha em produção)
        // window.musicPlayer.loadPlaylist(examplePlaylist);
    }
});
