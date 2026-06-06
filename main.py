import yaml
import os
import pandas as pd
from psychopy import visual
from psychopy.hardware import keyboard
import random


# Załadowanie ustawień z pliku .yaml: funkcja load_config
def load_config(file_name):
    with open(file_name, encoding="utf-8") as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

# Zdefiniowanie obiektów: win, klawiatura, bodźce, grafiki z instrukcją,
# grafiki z feedbackiem

win = visual.Window(fullscr = False, color = (load_config()["screen_color"]), units = 'pix', checkTiming = False)
kb = keyboard.Keyboard()
stim_bc = # niebieskie koło
stim_gc = # zielone koło
stim_bt = # niebieski trójkąt
stim_gt = # zielony trójkąt
stim_list = [stim_bc, stim_gc, stim_bt, stim_gt]
feedback_correct = # poprawna odpowiedź
feedback_incorrect =  # błędna odpowiedź
feedback_timeout = # za wolno

# Poprawne odpowiedzi

answers_color = {stim_bc: "k", stim_gc: "d", stim_bt: "k", stim_gt: "d"}
# niebieski - k; zielony - d
answers_shape = {stim_bc: "d", stim_gc: "d", stim_bt: "k", stim_gt: "k"}
# koło - d, trójkąt - k


# Losowanie bodźców: funkcja make_stim_list
def make_stim_list(n,# n - liczba bodźców do wygenerowania
                   mixed_trial = False): # mixed_trial - wskazuje, czy mamy do czynienia z próbą mieszaną

    opts = stim_list.copy()
    stim_queue = []
    quota = {}
    m = (n - n % 4)

    for i in opts:
        quota[i] = int(m / 4)
    # zapewniamy równoliczność (tak bardzo jak to możliwe) poszczególnych bodźców

    stim_queue.append(random.choice(opts))
    quota[stim_queue[0]] = quota[stim_queue[0]] - 1

    for i in range(m - 1):
        if quota[stim_queue[i]] == 0 and stim_queue[i] in opts:
            opts.remove(stim_queue[i])
        curr_opts = opts.copy()
        if stim_queue[i] in opts:
            curr_opts.remove(stim_queue[i])
        stim_queue.append(random.choice(curr_opts))
        quota[stim_queue[i + 1]] = quota[stim_queue[i + 1]] - 1

    if m != n:
        for i in range(m - 1, n - 1):
            opts = stim_queue.copy()
            curr_opts = opts.copy()
            if stim_queue[i] in opts:
                curr_opts.remove(stim_queue[i])
            stim_queue.append(random.choice(curr_opts))

    # losujemy n bodźców tak, by nie powtarzały się jedno po drugim
    # czyli jeśli stims[i] = stim1 to stims[i+1] != stim1 i stims[i-1] != stim1
    # zdefiniowanie tego jako funkcji pozwoli nam uniknąć pisania tego samego
    # 32873529 razy: po prostu przywołujemy kod za każdym razem, gdy musimy
    # stworzyć listę bodźców

    focus_times = [random.randint(400, 700) for _ in range(n)]

    #losujemy n czasów wyświetlania się punktów fiksacji

    if mixed_trial:
        l = (n - 1) - (n-1)%2
        switch_opts = [True, False]
        switch_queue = []
        switch_quota = {}

        trial_type_queue = []

        for i in switch_opts:
            switch_quota[i] = l/2

        switch_queue.append(random.choice(switch_opts))
        switch_quota[switch_queue[0]] = switch_quota[switch_queue[0]] - 1

        for i in range(l - 1):
            if switch_quota[switch_queue[i]] == 0:
                switch_opts.remove(switch_queue[i])
            switch_queue.append(random.choice(switch_opts))
            switch_quota[switch_queue[i + 1]] = switch_quota[switch_queue[i + 1]] - 1

        if l != n-1:
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

        # ok nie wiem czy to najlepszy sposób, ale na ten moment jest jedyny więc
        # najlepszy by default :P
        # proponuję wygenerować najpierw listę pomocniczą n-1 wartości logicznych
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



def check_correct(stim, #stim - rodzaj bodźca
                  trial_type, # trial_type - typ próby (shape/color)
                  focus_time,  # focus_time - czas wyświetlania punktu fiksacji
                  # (losowany),

                  #zadane, nie będziemy ich zmieniać

                  reaction_time = load_config(),
                  #reaction_time - czas na odpowiedź (z load_config)
                  cue_time = load_config()):
                              # cue_time - czas wyświetlania wskazówki (z load_config)
    # tu kod

    # Czekamy na odpowiedź przez zadany czas (reaction_time)

    # Funkcja zwraca zmienne:
    # answered - czy odpowiedź została udzielona (True/False)
    # correct_answer - czy udzielona odpowiedź jest poprawna (True/False)


def give_feedback():
    # tu kod

    # Funkcja wyświetla odpowiedni feedback:
    # answered = False: ZA WOLNO
    # answered = True i correct_answer = False: ŹLE
    # answered = True i correct_answer = True: DOBRZE

def save_data(result_list,
              ...,
              mixed_trial = False): #jeszcze inne zmienne

    individual_result = {}
    # tu kod

    #tworzy słownik individual_result, następnie dodaje go do listy
    if not mixed_trial:
        # Zawsze trial REPEAT

    else:
        # Trial REPEAT lub SWITCH

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


def practice_run_single(n, # n - ilość bodźców
                 trial_type): # trial_type - typ próby

    make_stim_list(n)

    # funkcja zwraca listy stims, focus_times

    for i in range(n):
        # Zadajemy zmienne stim, focus_time

        stim = stims[i]
        focus_time = focus_times[i]

        # Resetujemy zmienne

        answered = False
        correct_answer = False

        check_correct(stim = stim,
                      trial_type = trial_type,
                      focus_time = focus_time)
        give_feedback()

        # Podczas treningu dajemy feedback i nie zapisujemy odpowiedzi

def testing_run_single(n, # n - ilość bodźców
                 trial_type, # trial_type - typ próby
                 results): #lista, do ktorej zapisujemy wyniki

    make_stim_list(n)

    # funkcja zwraca listy stims, focus_times

    for i in range(n):
        # Zadajemy zmienne stim, focus_time

        stim = stims[i]
        focus_time = focus_times[i]

        # Resetujemy zmienne

        answered = False
        correct_answer = False

        check_correct(stim = stim,
                      trial_type = trial_type,
                      focus_time = focus_time)

        save_data(result_list = results)

def practice_run_mixed(n):
    make_stim_list(n, mixed_trial = True)

    for i in range(n):

        stim = stims[i]
        focus_time = focus_times[i]
        trial_type = trial_types[i]

        answered = False
        correct_answer = False

        check_correct(stim = stim,
                      trial_type = trial_type,
                      focus_time = focus_time)

        give_feedback()

def testing_run_mixed(n,
                      results):
    make_stim_list(n, mixed_trial = True)

    for i in range(n):

        stim = stims[i]
        focus_time = focus_times[i]
        trial_type = trial_types[i]

        answered = False
        correct_answer = False

        check_correct(stim = stim,
                      trial_type = trial_type,
                      focus_time = focus_time)

        save_data(result_list=results, mixed_trial=True)



# Wyświetlenie instrukcji

def trial(single_training_n = load_config(),
          # ilość bodźców wyświetlanych podczas treningu kolor i treningu kształt
          # (z load_config)
          single_trial_n = load_config(),
          # ilość bodźców wyświetlanych podczas próby kolor i próby kształt
          # (z load_config)
          mixed_training_n = load_config(),
          # ilość bodźców wyświetlanych podczas treningu mieszanego
          # (z load_config)
          mixed_trial_n = load_config()):
          # ilość bodźców wyświetlanych podczas próby mieszanej
          # (z load_config)

    # Utworzenie listy na wyniki prób

    results = []

    # TRENING KOLOR

    # Wyświetlenie informacji o rozpoczęciu treningu KOLOR

    practice_run_single(single_training_n, "color")

    # Wyświetlenie informacji o zakończeniu treningu KOLOR

# ///////////////////////////////////////////////////

    #PRÓBA KOLOR

    # Wyświetlenie informacji o rozpoczęciu badania KOLOR

    testing_run_single(single_trial_n, "color", results = results)

    # Wyświetlenie informacji o zakończeniu badania KOLOR

# ///////////////////////////////////////////////////
    # TRENING KSZTAŁT

    # Wyświetlenie informacji o rozpoczęciu treningu KSZTAŁT

    practice_run_single(single_training_n, "shape")

    # Wyświetlenie informacji o zakończeniu treningu KSZTAŁT

# ///////////////////////////////////////////////////

    #PRÓBA KSZTAŁT

    # Wyświetlenie informacji o rozpoczęciu badania KSZTAŁT

    testing_run_single(single_trial_n, "shape", results = results)

    # Wyświetlenie informacji o zakończeniu badania KSZTAŁT

# ///////////////////////////////////////////////////
    # TRENING MIESZANE

    # Wyświetlenie informacji o rozpoczęciu treningu MIESZANE

    practice_run_mixed(mixed_training_n)

    # Wyświetlenie informacji o zakończeniu treningu MIESZANE

# ///////////////////////////////////////////////////

    #PRÓBA MIESZANE

    # Wyświetlenie informacji o rozpoczęciu badania MIESZANE

    testing_run_mixed(mixed_trial_n, results = results)

    # Wyświetlenie informacji o zakończeniu badania MIESZANE

# ///////////////////////////////////////////////////

    save_tofile(results, "file_name", "results")

