import random
import sys

import pygame


class CodeSnippet:
    def __init__(self, text, is_mutable):
        if text == '    ':
            text = '     '
        self.text = text
        self.is_mutable = is_mutable


class CodeBlock:
    def __init__(self):
        self.snippets = []
        self.mutable_indices = []
        self.newline_indices = set()
        self.mutated_index = -1

    def add(self, text, is_mutable=False):
        if is_mutable:
            self.mutable_indices.append(len(self.snippets))
        self.snippets.append(CodeSnippet(text, is_mutable))

    def newline(self):
        self.newline_indices.add(len(self.snippets))

    def generate_code_lines(self):
        lines = []
        line = ''
        if self.snippets:
            self.mutated_index = random.choice(self.mutable_indices)
        for i, snippet in enumerate(self.snippets):
            if i in self.newline_indices:
                lines.append(line)
                line = ''
            added_text = snippet.text if i != self.mutated_index else ('?' * len(snippet.text))
            line += added_text
        if line != '':
            lines.append(line)
        return lines


pygame.init()
screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Family Day Game')

font = pygame.font.SysFont('consolas', 20)

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

margin = 10
input_height = int(screen_height * 0.2)
score_height = int(screen_height * 0.1)
display_height = screen_height - input_height - score_height


def main():
    cb = CodeBlock()
    cb.add("while (TSMC.Globalization(")
    cb.add("True", True)
    cb.add("))")
    cb.newline()
    cb.add("{")
    cb.newline()
    cb.add("     newFab = ")
    cb.add("tsmc", True)
    cb.add(".createNewFab(")
    cb.add("F21@Arizona", True)
    cb.add(");")
    cb.newline()
    cb.add("          for (services in IT Platforms)")
    cb.newline()
    cb.add("          {")
    cb.newline()
    cb.add("          F21.deploy(newFab);")
    cb.newline()
    cb.add("     newFab.Run();")
    cb.add("}")

    score = 0
    input_text = ''
    answer_status = ''
    clock = pygame.time.Clock()
    code_lines = cb.generate_code_lines()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    print(f"input_text = {input_text}")
                    if cb.mutated_index != -1 and cb.snippets[cb.mutated_index].text == input_text:
                        score += 1
                        answer_status = "Correct!!!"
                    else:
                        answer_status = "Wrong :("
                    input_text = ''
                else:
                    input_text += event.unicode
        screen.fill(WHITE)
        y_offset = 10
        for line in code_lines:
            code_surface = font.render(line, True, BLACK)
            screen.blit(code_surface, (10, y_offset))
            y_offset += font.get_height() + 5

        score_surface = font.render(f"Score: {score}", True, BLACK)
        answer_status_surface = font.render(answer_status, True, BLACK)

        screen.blit(score_surface, (10, display_height + 10))
        screen.blit(answer_status_surface, (10, display_height - 60))
        input_box_rect = pygame.Rect(
            margin,
            screen_height - input_height + margin,
            screen_width - 2 * margin,
            input_height - 2 * margin
        )
        pygame.draw.rect(screen, GRAY, input_box_rect)
        pygame.draw.rect(screen, BLACK, input_box_rect, 2)
        input_surface = font.render(input_text, True, BLACK)
        screen.blit(input_surface, (
            input_box_rect.x + 5, input_box_rect.y + (input_box_rect.height - font.get_height()) // 2))
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
