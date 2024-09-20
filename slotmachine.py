import pygame
import random

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Slot Machine Simulation")

pygame.font.init()
font = pygame.font.SysFont("Arial", 24)

symbols_images = {
    "Apple": pygame.image.load("Assets/Apple.png"),
    "Berry": pygame.image.load("Assets/Berry.png"),
    "Orange": pygame.image.load("Assets/Orange.png"),
    "Leamon": pygame.image.load("Assets/Leamon.png"),
    "Jackpot": pygame.image.load("Assets/Jackpot.png")
}

symbols_images = {symbol: pygame.transform.scale(image, (50, 50)) for symbol, image in symbols_images.items()}

symbols = ['Apple', 'Berry', 'Orange', 'Leamon', 'Jackpot']
symbol_frequencies = [5, 4, 3, 2, 1]
symbol_payouts = {
    'Apple': 2,
    'Berry': 3,
    'Orange': 5,
    'Leamon': 8,
    'Jackpot': 50
}

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

total_winnings = 0
jackpot_wins = 0
total_spins = 0
bet_per_spin = 1
clock = pygame.time.Clock()

def get_number_of_spins():
    input_box = pygame.Rect(100, 400, 200, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False
    spins = 0

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                return 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        spins = int(text) if text.isdigit() else 10
                        return spins
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(WHITE)
        txt_surface = font.render("Enter number of spins:", True, BLACK)
        screen.blit(txt_surface, (100, 350))

        txt_surface = font.render(text, True, color)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)

def spin_reels():
    reel_result = []
    for _ in range(3):
        column = [random.choices(symbols, symbol_frequencies)[0] for _ in range(3)]
        reel_result.append(column)
    return reel_result

def check_payout(middle_row):
    global jackpot_wins, total_winnings
    payout = 0
    if middle_row[0] == middle_row[1] == middle_row[2]:
        symbol = middle_row[0]
        payout = symbol_payouts[symbol]
        total_winnings += payout
        if symbol == 'Jackpot':
            jackpot_wins += 1
    return payout

def display_results(reel_results, spin_num):
    screen.fill(WHITE)
    grid_size = 50
    grid_spacing = 10
    grid_width = (grid_size * 3) + (grid_spacing * 2)
    grid_height = (grid_size * 3) + (grid_spacing * 2)

    start_x = (SCREEN_WIDTH - grid_width) // 2
    start_y = (SCREEN_HEIGHT - grid_height) // 2

    for row in range(3):
        for col in range(3):
            symbol_image = symbols_images[reel_results[col][row]]
            screen.blit(symbol_image, (start_x + col * (grid_size + grid_spacing), start_y + row * (grid_size + grid_spacing)))

    spin_text = font.render(f"Spin: {spin_num + 1}", True, BLUE)
    screen.blit(spin_text, (10, 10))

    pygame.display.flip()

def display_final_stats():
    screen.fill(WHITE)
    final_text = font.render(f"Final RTP: {calculate_rtp(total_spins):.2f}%", True, BLACK)
    screen.blit(final_text, (100, 250))

    jackpot_text = font.render(f"Total Jackpot Wins: {jackpot_wins}", True, BLACK)
    screen.blit(jackpot_text, (100, 300))

    total_winnings_text = font.render(f"Total Winnings: {total_winnings}", True, BLACK)
    screen.blit(total_winnings_text, (100, 350))

    pygame.display.flip()
    pygame.time.wait(5000)

def calculate_rtp(spins):
    if spins == 0:
        return 0
    return total_winnings / (spins * bet_per_spin) * 100

def main():
    global total_winnings, jackpot_wins, total_spins

    n_spins = get_number_of_spins()

    if n_spins == 0:
        return

    run_simulation = True
    total_winnings = 0
    jackpot_wins = 0
    total_spins = n_spins

    for spin_num in range(n_spins):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_simulation = False
                pygame.quit()
                return

        reel_results = spin_reels()
        display_results(reel_results, spin_num)
        check_payout([reel_results[i][1] for i in range(3)])

        pygame.time.wait(1000)
        clock.tick(30)

    display_final_stats()

if __name__ == "__main__":
    main()
    pygame.quit()
