from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pickle
import requests

USE_TONE = False

URL_SYLLABLE_TONE = 'https://lingua.mtsu.edu/chinese-computing/phonology/syllabletone.php'
URL_SYLLABLE = 'https://lingua.mtsu.edu/chinese-computing/phonology/syllable.php'
FILENAME_SYLLABLE_TONE = 'syllable_tone.pkl'
FILENAME_SYLLABLE = 'syllable.pkl'
SORTED_FREQS_TONE_FILENAME = 'sorted_freqs_tone.pkl'
SORTED_FREQS_FILENAME = 'sorted_freqs.pkl'
PLOT_TONES = 'plot_tones.png'
PLOT = 'plot.png'

filename = FILENAME_SYLLABLE_TONE if USE_TONE else FILENAME_SYLLABLE
sorted_freqs_filename = SORTED_FREQS_TONE_FILENAME if USE_TONE else SORTED_FREQS_FILENAME
plot = PLOT_TONES if USE_TONE else PLOT

def scrape_data():
    """Scrape data from website table."""
    def is_valid_row(row):
        # only the rows starting with a number are valid, the others contain spans or breaks
        return str(row)[0] in '0123456789'

    SYLLABLE_INDEX = 1
    FREQ_INDEX = 2

    url = URL_SYLLABLE_TONE if USE_TONE else URL_SYLLABLE

    response = requests.get(url)

    if response.ok:
        soup = BeautifulSoup(response.text, "lxml")
        table = soup.find("pre") 
        syllable_to_count = {}
        for row in table.children:
            if is_valid_row(row):
                split_row = row.split('\t')
                syllable = split_row[SYLLABLE_INDEX]
                freq = split_row[FREQ_INDEX]

                syllable_to_count[syllable] = int(freq)
    
    with open(filename, 'wb') as f: 
        pickle.dump(syllable_to_count, f) 

def analyze_data():
    """Generate sorted list of frequencies by syllable."""
    # load file
    with open(filename, 'rb') as f:
        syllable_to_count = pickle.load(f)
        
        # generate sorted list of freqs by syllable
        total = 0
        for count in syllable_to_count.values():
            total += count

        syllable_to_freq = {}
        for syllable, count in syllable_to_count.items():
            syllable_to_freq[syllable] = count / total
        
        items = syllable_to_freq.items()
        sorted_freqs = sorted(items, key=lambda x: x[1], reverse=True)

        with open(sorted_freqs_filename, 'wb') as f2: 
            pickle.dump(sorted_freqs, f2) 

def display_data():
    # load file
    with open(sorted_freqs_filename, 'rb') as f:
        sorted_freqs = pickle.load(f)

        # display data
        limit = 10
        syllables = [x[0] for x in sorted_freqs[:limit]]
        freqs = [x[1] for x in sorted_freqs[:limit]]

        plt.bar(syllables, freqs)
        if limit > 10:
            plt.xticks(rotation=45, ha='right')
        plt.xlabel('Pronunciation')
        plt.ylabel('Frequency')
        plt.title('Mandarin Syllable Frequency by Frequency of Occurrence in Corpus')
        plt.savefig(plot)
        plt.show()





def main():
    display_data()

if __name__ == '__main__':
    main()