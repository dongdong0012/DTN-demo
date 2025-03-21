import os
import json
from collections import defaultdict
import math
from datetime import datetime, timedelta
from tqdm import tqdm



def read_tweet_time(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        if 'created_at' in data:
            tweet_time = datetime.strptime(data['created_at'], "%a %b %d %H:%M:%S %z %Y")
            return tweet_time
    return None



def read_tweet_times(folder):
    tweet_times = []
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        if filename.endswith('.json'):
            tweet_time = read_tweet_time(filepath)
            if tweet_time:
                tweet_times.append(tweet_time)
    return tweet_times

def calculate_smoothed_entropy(times, start_time, end_time, delta, alpha=1):
    time_slots = defaultdict(int)
    current_time = start_time
    while current_time < end_time:
        next_time = current_time + delta
        for time in times:
            if current_time <= time < next_time:
                time_slots[current_time] += 1
        current_time = next_time

    total_count = sum(time_slots.values())
    smoothed_entropy = 0
    for count in time_slots.values():

        p = (count + alpha) / (total_count + alpha * len(time_slots))
        if p > 0:
            smoothed_entropy -= p * math.log(p, 2)
    return smoothed_entropy

def analyze_directory(base_dir, delta, output_base_dir):
    for event_folder in os.listdir(base_dir):
        if event_folder.endswith('-all-rnr-threads'):
            for rumority in ['rumours', 'non-rumours']:
                rumor_path = os.path.join(base_dir, event_folder, rumority)


                all_entropy_data = []

                for news_id in tqdm(os.listdir(rumor_path), desc=f'{event_folder}-{rumority}'):
                    if news_id == '.DS_Store':
                        continue
                    news_root = os.path.join(rumor_path, news_id)
                    source_tweet_path = os.path.join(news_root, 'source-tweet', f'{news_id}.json')


                    start_time = read_tweet_time(source_tweet_path)
                    if start_time:

                        reaction_path = os.path.join(news_root, 'reactions')
                        tweet_times = read_tweet_times(reaction_path)

                        if tweet_times:
                            end_time = max(tweet_times) + timedelta(days=1)
                            entropy = calculate_smoothed_entropy(tweet_times, start_time, end_time, delta)


                            all_entropy_data.append({
                                "news_id": news_id,
                                "entropy": entropy
                            })


                save_all_entropies(output_base_dir, event_folder, rumority, all_entropy_data)


def save_all_entropies(output_base_dir, event_folder, rumority, all_entropy_data):
    output_dir = os.path.join(output_base_dir, event_folder)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    output_file = os.path.join(output_dir, f'{rumority}_entropy.json')
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(all_entropy_data, file, ensure_ascii=False, indent=4)
    print(f'All entropies for {event_folder}/{rumority} saved to {output_file}')


# 主函数
def main():
    base_directory = './PHEME'
    output_directory = './entropy'
    time_step = timedelta(hours=6)

    analyze_directory(base_directory, time_step, output_directory)


if __name__ == "__main__":
    main()
