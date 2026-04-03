import pygame
import sys
import pathlib

def start_application() -> None:
    pygame.init()
    pygame.mixer.init()
    big_font = pygame.font.SysFont('Arial', 22)
    small_font = pygame.font.SysFont('Arial', 18)
    width, height = 700, 700
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Music Player")
    clock = pygame.time.Clock()
    path = pathlib.Path(__file__).parent / "tracks"
    playlist = [str(song) for song in path.iterdir() if song.is_file() and ".mp3" in str(song) and "Empty Author - Empty Track" not in str(song)]
    if not playlist:
        return
    current_index = 0
    playing = False
    paused = False
    pygame.mixer.music.set_endevent(pygame.USEREVENT)

    def load_current():
        try:
            pygame.mixer.music.load(playlist[current_index])
        except IndexError:
            pygame.mixer.music.load(path / "Empty Author - Empty Track.mp3")

    def play_current():
        nonlocal playing, paused
        if paused:
            pygame.mixer.music.unpause()
            paused = False
        else:
            load_current()
            pygame.mixer.music.play()
        playing = True

    def stop_current():
        nonlocal playing, paused
        pygame.mixer.music.pause()
        playing = False
        paused = True

    def next_track():
        nonlocal current_index, paused
        try:
            current_index = (current_index + 1) % len(playlist)
        except ZeroDivisionError:
            current_index = 0
        paused = False
        load_current()
        pygame.mixer.music.play()

    def previous_track():
        nonlocal current_index, paused
        try:
            current_index = (current_index - 1) % len(playlist)
        except ZeroDivisionError:
            current_index = 0
        paused = False
        load_current()
        pygame.mixer.music.play()

    def delete_current():
        nonlocal current_index
        if len(playlist) > 1:
            playlist.pop(current_index)
            current_index %= len(playlist)
            load_current()
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.stop()
            playlist.clear()

    def reload_tracks():
        nonlocal playlist
        tracks = [str(song) for song in path.iterdir() if song.is_file() and ".mp3" in str(song) and "Empty Author - Empty Track" not in str(song)]
        playlist = list(dict.fromkeys(playlist + tracks))

    load_current()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                next_track()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    play_current()
                elif event.key == pygame.K_s:
                    stop_current()
                elif event.key == pygame.K_n:
                    next_track()
                    playing = True
                elif event.key == pygame.K_b:
                    previous_track()
                    playing = True
                elif event.key == pygame.K_d:
                    delete_current()
                elif event.key == pygame.K_r:
                    reload_tracks()
                elif event.key == pygame.K_q:
                    running = False
        screen.fill((255, 255, 255))
        if playlist:
            track_name = pathlib.Path(playlist[current_index]).name
        else:
            track_name = "Empty Author - Empty Track.mp3"
        text = big_font.render(f"Track: {track_name.replace(".mp3", "")}", True, (0, 0, 0))
        screen.blit(text, (50, 80))
        status = "Playing" if playing else "Paused"
        status_text = small_font.render(f"Status: {status}", True, (0, 0, 0))
        screen.blit(status_text, (50, 130))
        index_text = small_font.render(f"Index: {current_index + 1 if playlist else 0}/{len(playlist) if playlist else 0}", True, (0, 0, 0))
        screen.blit(index_text, (50, 180))
        if playing or paused:
            pos_ms = pygame.mixer.music.get_pos()
            pos_sec = pos_ms // 1000
        else:
            pos_sec = 0
        progress_text = small_font.render(f"Position: {pos_sec} sec", True, (0, 0, 0))
        screen.blit(progress_text, (50, 230))
        controls = [
            "P - Play current",
            "S - Stop current",
            "N - Next track",
            "B - Previous track",
            "D - Delete current",
            "R - Reload tracks",
            "Q - Quit application"
        ]
        for index, line in enumerate(controls):
            control_text = small_font.render(line, True, (0, 0, 0))
            screen.blit(control_text, (50, 300 + index * 30))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    start_application()
