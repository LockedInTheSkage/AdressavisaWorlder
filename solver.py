import math
import json

class Solver:
    @staticmethod
    def simulate_game(answer=None):
        common_words = []
        if answer:
            common_words = [answer]
        else:
            with open("common_words.txt") as file:
                for line in file:
                    word = line[:-1]
                    word = word.replace('Ã¥', 'å')
                    word = word.replace('Ã¸', 'ø')
                    word = word.replace('Ã¦', 'æ')
                    common_words.append(word)
            common_words = common_words[1:300]
        words_by_guesses = {}

        total_word_list = []

        with open("ordliste.txt") as file:
            for line in file:
                word = line[:-1]
                word = word.replace('Ã¥', 'å')
                word = word.replace('Ã¸', 'ø')
                word = word.replace('Ã¦', 'æ')
                total_word_list.append(word)

        for i, word in enumerate(common_words):
            Solver.update_loading_bar(i, len(common_words))
            previous_guesses = []
            remaining_word_list = total_word_list
            input_result = 0

            while input_result < 3 ** 5 - 1:
                first_attempt, word_buckets = Solver.find_best_word(remaining_word_list, previous_guesses, show_loading_bar=False)
                if first_attempt == "No word found":
                    break
                input_result = Solver.test_result(word, first_attempt)
                if input_result == 3 ** 5 - 1:
                    break
                remaining_word_list = word_buckets[input_result]
                previous_guesses.append((first_attempt, input_result))

            if first_attempt == "No word found":
                words_by_guesses["No word found"] = [word]
            else:
                guesses = str(len(previous_guesses)+1)
                if guesses in words_by_guesses:
                    words_by_guesses[guesses].append(word)
                else:
                    words_by_guesses[guesses] = [word]

        guess_counts = {}
        most_common_amount = 0
        total_count=0
        guessesList=[]
        for guesses, words in words_by_guesses.items():
            guess_counts[guesses] = len(words)
            total_count+=len(words)
            guessesList.append("Nothing" if guesses == "No word found" else int(guesses))
            if len(words) > most_common_amount:
                most_common_amount = len(words)

        print("Guess counts:")
        treshholds=most_common_amount/20
        guessesList.sort()
        for guesses in guessesList:
            count=guess_counts[str(guesses)]
            string=f"{guesses}:["+"#"*int(count//treshholds)+"-"*int(20-count//treshholds)+"]"+f" {count}/{(10000*count/total_count)//100}"+"%"
            print(string)

    @staticmethod
    def play_game():
        total_word_list=[]

        with open("ordliste.txt") as file:
            for line in file:
                word=line[:-1]
                word=word.replace('Ã¥','å')
                word=word.replace('Ã¸','ø')
                word=word.replace('Ã¦','æ')
                total_word_list.append(word)

        previous_guesses=[]
        remaining_word_list=total_word_list
        input_result=0
        while  input_result<3**5-1:
            print("Looking for the best word")
            first_attempt, word_buckets=Solver.find_best_word(remaining_word_list, previous_guesses)
            if first_attempt=="No word found":
                break
            print("The best word is: ", first_attempt)
            input_result_str=input("Enter the score of the guess: ")
            while len(input_result_str)!=5 or not input_result_str.isnumeric():
                print("Invalid input, please enter a 5 letter string of 0, 1 and 2")
                print("0: The letter is not in the word")
                print("1: The letter is in the word, but not in the right position")
                print("2: The letter is in the word and in the right position")
                input_result_str=input("Enter the score of the guess: ")
            input_result=Solver.input_result_int(input_result_str)
            if input_result==3**5-1:
                break
            remaining_word_list=word_buckets[input_result]
            previous_guesses.append((first_attempt,input_result))

        if first_attempt=="No word found":
            print(first_attempt)
        else:
            print(f"Thank you for playing the game, the word was: {first_attempt} and it took {len(previous_guesses)} guesses to find it")

    @staticmethod
    def input_result_int(input_result_str):
        int_result=0

        for i, value in enumerate(input_result_str):
            if value not in ["0","1","2"]:
                print("Invalid input, please enter a string of 0, 1 and 2")
                return Solver.input_result_int(input("Enter the score of the guess: "))
            int_result+=int(value)*3**i

        return int_result

    @staticmethod
    def find_best_word(word_list, previous_guesses, show_loading_bar=True):
        if len(word_list)==1:
            return word_list[0], []
        elif len(word_list)==0:
            return "No word found", []

        best_word=":|"
        best_variance=math.inf

        candidate_word, word_buckets, variance = Solver.access_cache(previous_guesses)
        if variance!=math.inf:
            return candidate_word, word_buckets

        for i, candidate_word in enumerate(word_list):
            if show_loading_bar:
                Solver.update_loading_bar(i,len(word_list))
            other_word_list=word_list.copy()
            other_word_list.remove(candidate_word)

            word_buckets=Solver.sort_to_buckets(other_word_list, candidate_word)
            variance=Solver.variance_of(word_buckets)
            if variance<best_variance:
                best_variance=variance
                best_word=candidate_word
                best_buckets=word_buckets

        Solver.update_cache(previous_guesses, best_word, best_buckets, best_variance)

        return best_word, best_buckets

    @staticmethod
    def access_cache(previous_guesses):
        cache = Solver.load_cache()
        key=str(previous_guesses)
        if cache is None:
                cache = Solver.create_cache()

        if key in cache:
            candidate_word = cache[key]['candidate_word']
            word_buckets = cache[key]['buckets']
            variance = cache[key]['variance']
        else:
            candidate_word =""
            word_buckets = []
            variance = math.inf

        return candidate_word, word_buckets, variance

    @staticmethod
    def update_cache(previous_guesses, candidate_word, word_buckets, variance):
        cache = Solver.load_cache()
        key=str(previous_guesses)
        if cache is None:
            cache = Solver.create_cache()

        cache[key] = {
            'candidate_word': candidate_word,
            'buckets': word_buckets,
            'variance': variance
        }

        Solver.save_cache(cache)

    @staticmethod
    def load_cache():
        try:
            with open("cache.json", "r") as file:
                cache = json.load(file)
            return cache
        except FileNotFoundError:
            return None

    @staticmethod
    def save_cache(cache):
        with open("cache.json", "w") as file:
            json.dump(cache, file)

    @staticmethod
    def create_cache():
        return {}

    @staticmethod
    def update_loading_bar(i,n):
        treshholds=n/20
        string="["+"#"*int(i//treshholds)+"-"*int(20-i//treshholds)+"]"+" "+str(int(i/n*10000)/100)+"%"
        print(string,end="\r")
        if i==n-1:
            print("["+"#"*20+"]")

    @staticmethod
    def sort_to_buckets(word_list, candidate_word):
        buckets=[[].copy() for r in range(3**5)]

        for word_for_bucket in word_list:
            hash_index=Solver.test_result(word_for_bucket,candidate_word)
            buckets[hash_index].append(word_for_bucket)

        return buckets

    @staticmethod
    def variance_of(word_buckets):
        bucket_sizes=Solver.bucket_size_of(word_buckets)
        avg=sum(bucket_sizes)/len(bucket_sizes)
        V=0
        for size in bucket_sizes:
            V+=(size-avg)**2
        V=V/len(bucket_sizes)
        V=math.sqrt(V)
        return V

    @staticmethod
    def bucket_size_of(word_buckets):
        return [len(bucket) for bucket in word_buckets]

    @staticmethod
    def test_result(answer, attempt):
        result=0
        attempt_misses=""
        answer_misses=""

        for i, letter in enumerate(attempt):
            if attempt[i] == answer[i]:
                result+=2*3**i
                attempt_misses+="!"
                answer_misses+="!"
            else:
                attempt_misses+=letter
                answer_misses+=answer[i]

        for i, letter in enumerate(attempt_misses):
            if letter in answer_misses and letter!="!":
                result+=3**i

        return result    