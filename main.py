import yaml
import os
import pandas as pd
from psychopy import visual, core
from psychopy.hardware import keyboard
import random
import time

global_trial_number = 0

# Załadowanie ustawień z pliku .yaml: funkcja load_config
def load_config(file_name="config.yaml"):
    with open(file_name, encoding="utf-8") as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

_config_defaults = load_config()

win = visual.Window(
    size=_config_defaults["screen_size"],
    fullscr=_config_defaults["fullscr"],
    color=_config_defaults["screen_color"],
    units=_config_defaults["unit"],
    checkTiming=_config_defaults["checkTiming"]
)
kb = keyboard.Keyboard()

stim_bc = visual.Circle(win, radius=_config_defaults["circle_radius_1"], fillColor=_config_defaults["circle_color_1"], lineColor=None)
stim_gc = visual.Circle(win, radius=_config_defaults["circle_radius_2"], fillColor=_config_defaults["circle_color_2"], lineColor=None)

stim_bs = visual.Rect(win, width=_config_defaults["square_size_1"], height=_config_defaults["square_size_1"], fillColor=_config_defaults["square_color_1"], lineColor=None)
stim_gs = visual.Rect(win, width=_config_defaults["square_size_2"], height=_config_defaults["square_size_2"], fillColor=_config_defaults["square_color_2"], lineColor=None)

stim_list = [stim_bc, stim_gc, stim_bs, stim_gs]

stim_names = {
    stim_bc: "blue_circle",
    stim_gc: "green_circle",
    stim_bs: "blue_square",
    stim_gs: "green_square",
}
#Punkt fiksacji (biały krzyżyk)
fixation = visual.TextStim(win, text='+', color=_config_defaults["fixation_point_color"], height = _config_defaults["fixation_point_height"])

#  Wskazówki
cue_bg = visual.Rect(win, width=_config_defaults["cue_bg_width"], height=_config_defaults["cue_bg_height"], fillColor=_config_defaults["cue_bg_fillColor"], lineColor=_config_defaults["cue_bg_lineColor"], lineWidth=_config_defaults["cue_bg_lineWidth"])
cue_text_color = visual.TextStim(win, text='KOLOR', color=_config_defaults["cue_text_color_text_color"], height=_config_defaults["cue_text_color_height"], bold=_config_defaults["cue_text_color_isBold"])
cue_text_shape = visual.TextStim(win, text='KSZTAŁT', color=_config_defaults["cue_text_shape_text_color"], height=_config_defaults["cue_text_shape_height"], bold=_config_defaults["cue_text_shape_isBold"])

#  Feedback 
feedback_correct = visual.TextStim(win, text='✓', color=_config_defaults["feedback_correct_color"], height=_config_defaults["feedback_correct_height"])
feedback_incorrect = visual.TextStim(win, text='✗', color=_config_defaults["feedback_incorrect_color"], height=_config_defaults["feedback_incorrect_height"])
feedback_timeout = visual.TextStim(win, text='ZA WOLNO', color=_config_defaults["feedback_timeout_color"], height=_config_defaults["feedback_timeout_height"])

# Poprawne odpowiedzi
answers_color = {stim_bc: _config_defaults["key_2"], stim_gc: _config_defaults["key_1"], stim_bs: _config_defaults["key_2"], stim_gs: _config_defaults["key_1"]}
answers_shape = {stim_bc: _config_defaults["key_1"], stim_gc: _config_defaults["key_1"], stim_bs: _config_defaults["key_2"], stim_gs: _config_defaults["key_2"]}




# Losowanie bodźców: funkcja make_stim_list
def make_stim_list(n, mixed_trial=False):
    # m to wielokrotność liczby 4 (dla równego podziału)
    m = n - (n % 4)

    while True:
        # ustawiamy bazowe limity dla każdego bodźca
        quota = {s: m // 4 for s in stim_list}

        # jeśli n nie dzieli się idealnie przez 4, dodajemy losowe unikalne bodźce jako dopełnienie
        if n % 4 != 0:
            extra_opts = random.sample(stim_list, n % 4)
            for s in extra_opts:
                quota[s] += 1

        stim_queue = []
        failed = False

        for _ in range(n):
            # filtrujemy bodźce, które mają jeszcze wolną kwotę (częstość > 0)
            available = [s for s, q in quota.items() if q > 0]

            # zapobiegamy powtórzeniom pod rząd (usuwamy ostatnio dodany bodziec z dostępnych opcji)
            if stim_queue:
                available = [s for s in available if s != stim_queue[-1]]

            # jeśli wpadliśmy w ślepy zaułek (brak alternatywnych opcji), przerywamy i losujemy od nowa
            if not available:
                failed = True
                break

            chosen = random.choice(available)
            stim_queue.append(chosen)
            quota[chosen] -= 1

        # jeśli udało się wygenerować całą listę bez błędu, wychodzimy z pętli while
        if not failed:
            break

    # losujemy n czasów wyświetlania się punktów fiksacji
    focus_times = [random.randint(400, 700) for _ in range(n)]

    # sekcja dla prób mieszanych
    if mixed_trial:
        l = (n - 1) - (n - 1) % 2
        switch_opts = [True, False]
        switch_queue = []
        switch_quota = {}
        trial_type_queue = []

        for i in switch_opts:
            switch_quota[i] = l / 2

        switch_queue.append(random.choice(switch_opts))
        switch_quota[switch_queue[0]] = switch_quota[switch_queue[0]] - 1

        for i in range(l - 1):
            if switch_quota[switch_queue[i]] == 0:
                if switch_queue[i] in switch_opts:
                    switch_opts.remove(switch_queue[i])
            switch_queue.append(random.choice(switch_opts))
            switch_quota[switch_queue[i + 1]] = switch_quota[switch_queue[i + 1]] - 1

        if l != n - 1:
            switch_opts = [True, False]
            switch_queue.append(random.choice(switch_opts))

        trial_type_queue.append(random.choice(["color", "shape"]))

        for switch in switch_queue:
            if switch:
                if trial_type_queue[-1] == "color":
                    trial_type_queue.append("shape")
                else:
                    trial_type_queue.append("color")
            else:
                if trial_type_queue[-1] == "color":
                    trial_type_queue.append("color")
                else:
                    trial_type_queue.append("shape")

        switch_queue.insert(0, None)

        return stim_queue, focus_times, switch_queue, trial_type_queue

    else:
        return stim_queue, focus_times


        # wygenerować najpierw listę pomocniczą n-1 wartości logicznych
        # (czyli True/False)
        # a następnie:
        # 1. losujemy color/shape (typ pierwszej próby)
        # 2. jeśli switch = true, następny element będzie odmienny
        # 3. jeśli false to taki sam
        # i w taki sposób otrzymamy listę trial_types

# Podsumowując, funkcja zwraca:
    # listę bodźców stim_queue
    # listę czasów wyświetlania punktów fiksacji focus_times
    # w próbach mieszanych:
        # listę pomocniczą switch_queue
        # listę typów prób trial_type_queue


def check_correct(stim, trial_type, focus_time, reaction_time=1500, cue_time=600):
            global answered, correct_answer, rt, response_key

            kb.clearEvents()

            fixation.draw()
            win.flip()
            core.wait(focus_time / 1000.0)


            cue_bg.draw()
            if trial_type == "color":
                cue_text_color.draw()
            else:
                cue_text_shape.draw()
            win.flip()
            core.wait(cue_time / 1000.0)

            stim.draw()
            win.flip()

            kb.clock.reset()

            keys = kb.waitKeys(maxWait=reaction_time / 1000.0, keyList=['d', 'k'], waitRelease=False)


            if keys:
                answered = True
                response_key = keys[0].name
                rt = keys[0].rt * 1000.0

                if trial_type == "color":
                    correct_key = answers_color[stim]
                else:
                    correct_key = answers_shape[stim]

                if response_key == correct_key:
                    correct_answer = True
                else:
                    correct_answer = False
            else:
                answered = False
                correct_answer = False
                response_key = None
                rt = None
            return {
                "answered": answered,
                "correct_answer": correct_answer,
                "rt": rt,
                "response_key": response_key
            }



# Czekamy na odpowiedź przez zadany czas (reaction_time)

    # Funkcja zwraca zmienne:
    # answered - czy odpowiedź została udzielona (True/False)
    # correct_answer - czy udzielona odpowiedź jest poprawna (True/False)


def give_feedback():
    global answered, correct_answer
    if not answered:
        feedback_timeout.draw()
    elif correct_answer:
        feedback_correct.draw()
    else:
        feedback_incorrect.draw()

    win.flip()
    core.wait(0.5)
    win.flip()
    core.wait(0.5)

    # Funkcja wyświetla odpowiedni feedback:
    # answered = False: ZA WOLNO
    # answered = True i correct_answer = False: ŹLE
    # answered = True i correct_answer = True: DOBRZE

def save_data(result_list, block_name, stim, trial_type, is_switch, trial_results):
    global global_trial_number
    global_trial_number += 1

    if is_switch is None:
        transition = "NA"
    elif is_switch:
        transition = "SWITCH"
    else:
        transition = "REPEAT"

    congruency = "congruent" if answers_color[stim] == answers_shape[stim] else "incongruent"

    individual_result = {
        "Trial_Number": global_trial_number,
        "Block_Name": block_name,
        "Transition": transition,
        "Cue_Type": trial_type,
        "Stimulus": stim_names[stim],
        "Congruency": congruency,
        "Reaction_Time_ms": trial_results["rt"],
        "Correct": trial_results["correct_answer"],
        "Timeout": not trial_results["answered"],
        "Response_Key": trial_results["response_key"]
    }

    result_list.append(individual_result)



# do zarejestrowania:
    # numer kolejny próby w skali całego eksperymentu (od 1 do 200)
    # nazwa i typ aktualnej części badania
    # typ próby w kolejnych trialach (REPEAT/SWITCH)
    # rodzaj zaprezentowanego sygnału wskazującego aktualną regułę
    # cechy prezentowanego bodźca docelowego
    # stopień zgodności mapowania odpowiedzi (kongruentna/niekongruentna)
    # czas reakcji osoby badanej liczony od momentu pojawienia się bodźca
    # poprawność udzielonej odpowiedzi (lub przekroczenie czasu/timeout)
    # rodzaj udzielonej reakcji ("D"/"K")

def save_tofile(result_list,
              file_name,
              path = 'results'):
    os.makedirs(path, exist_ok=True)
    df = pd.DataFrame(result_list)
    df.to_csv(os.path.join(path, file_name), index=False)

    # Zapisuje wynik do pliku


def practice_run_single(n, trial_type):
    stims, focus_times = make_stim_list(n, mixed_trial=False)
    for i in range(n):
        stim = stims[i]
        focus_time = focus_times[i]
        answered = False
        correct_answer = False
        check_correct(stim=stim, trial_type=trial_type, focus_time=focus_time)
        give_feedback()

def testing_run_single(n, trial_type, results):
    stims, focus_times = make_stim_list(n, mixed_trial=False)
    for i in range(n):
        stim = stims[i]
        focus_time = focus_times[i]
        #trial_type = trial_types[i]
        #is_sw = switch_queue[i]
        trial_results = check_correct(stim=stim, trial_type=trial_type, focus_time=focus_time)
        save_data(result_list=results, block_name=f"Single_{trial_type}", stim=stim, trial_type=trial_type, is_switch=False, trial_results=trial_results)

def practice_run_mixed(n):
    stims, focus_times, switch_queue, trial_types = make_stim_list(n, mixed_trial=True)
    for i in range(n):
        stim = stims[i]
        focus_time = focus_times[i]
        trial_type = trial_types[i]
        answered = False
        correct_answer = False
        check_correct(stim=stim, trial_type=trial_type, focus_time=focus_time)
        give_feedback()

def testing_run_mixed(n, results):
    stims, focus_times, switch_queue, trial_types = make_stim_list(n, mixed_trial=True)
    for i in range(n):
        stim = stims[i]
        focus_time = focus_times[i]
        trial_type = trial_types[i]
        is_sw = switch_queue[i]

        trial_results = check_correct(stim=stim, trial_type=trial_type, focus_time=focus_time)

        save_data(result_list=results, block_name="Mixed_Block", stim=stim, trial_type=trial_type, is_switch=is_sw, trial_results=trial_results)



def show_instruction(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            text_content = f.read()
    else:
        text_content = f"Instrukcja z pliku '{file_name}'\n\nNaciśnij dowolny klawisz, aby kontynuować."
    if file_name=="instructions/instrukcja_glowna.txt":
        height = 16
    else:
        height = 24
    instr_stim = visual.TextStim(win, text=text_content, color='white', height=height,
        wrapWidth=800, alignText='center')
    instr_stim.draw()
    win.flip()

    kb.clearEvents()
    kb.waitKeys()  # Oczekiwanie na reakcję użytkownika
    win.flip()
    core.wait(0.5)

# Wyświetlenie instrukcji

def trial(single_training_n = _config_defaults["single_training_n"],
          # ilość bodźców wyświetlanych podczas treningu kolor i treningu kształt
          # (z load_config)
          single_trial_n = _config_defaults["single_trial_n"],
          # ilość bodźców wyświetlanych podczas próby kolor i próby kształt
          # (z load_config)
          mixed_training_n = _config_defaults["mixed_training_n"],
          # ilość bodźców wyświetlanych podczas treningu mieszanego
          # (z load_config)
          mixed_trial_n = _config_defaults["mixed_trial_n"]):
          # ilość bodźców wyświetlanych podczas próby mieszanej
          # (z load_config)

    # Utworzenie listy na wyniki prób

    results = []

    # INSTRUKCJA

    show_instruction("instructions/instrukcja_glowna.txt")

    # TRENING KOLOR

    # Wyświetlenie informacji o rozpoczęciu treningu KOLOR
    show_instruction("instructions/trening_kolor.txt")
    practice_run_single(single_training_n, "color")


# ///////////////////////////////////////////////////

    #PRÓBA KOLOR

    # Wyświetlenie informacji o rozpoczęciu badania KOLOR
    show_instruction("instructions/test_kolor.txt")
    testing_run_single(single_trial_n, "color", results = results)


# ///////////////////////////////////////////////////
    # TRENING KSZTAŁT

    # Wyświetlenie informacji o rozpoczęciu treningu KSZTAŁT
    show_instruction("instructions/trening_ksztalt.txt")
    practice_run_single(single_training_n, "shape")


# ///////////////////////////////////////////////////

    #PRÓBA KSZTAŁT

    # Wyświetlenie informacji o rozpoczęciu badania KSZTAŁT
    show_instruction("instructions/test_ksztalt.txt")
    testing_run_single(single_trial_n, "shape", results = results)

    # Wyświetlenie informacji o zakończeniu badania KSZTAŁT

# ///////////////////////////////////////////////////
    # TRENING MIESZANE

    # Wyświetlenie informacji o rozpoczęciu treningu MIESZANE
    show_instruction("instructions/trening_mieszane.txt")
    practice_run_mixed(mixed_training_n)



# ///////////////////////////////////////////////////

    #PRÓBA MIESZANE

    # Wyświetlenie informacji o rozpoczęciu badania MIESZANE
    show_instruction("instructions/test_mieszane.txt")
    testing_run_mixed(mixed_trial_n, results = results)

    # Wyświetlenie informacji o zakończeniu badania
    show_instruction("instructions/text_end.txt")
# ///////////////////////////////////////////////////

    current_time = time.strftime("%Y%m%d-%H%M%S")
    unique_filename = f"results_{current_time}.csv"

    save_tofile(results, unique_filename, "results")

if __name__ == "__main__":
    trial()
    win.close()
    core.quit()