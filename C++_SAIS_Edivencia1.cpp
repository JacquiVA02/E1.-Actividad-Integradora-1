#include <iostream>
#include <map>
#include <string>
#include <vector>

using namespace std;

map<char, pair<int, int>> getBuckets(const string& T) {
    map<char, int> count;
    map<char, pair<int, int>> buckets;

    // Contar la frecuencia de cada carácter
    for (char c : T) {
        count[c]++;
    }

    int start = 0;
    for (const auto& kv : count) {
        char c = kv.first;
        int frequency = kv.second;
        buckets[c] = make_pair(start, start + frequency);
        start += frequency;
    }

    return buckets;
}

int main() {
    string input = "exampleinput";
    map<char, pair<int, int>> result = getBuckets(input);

    // Imprimir los resultados
    for (const auto& kv : result) {
        char c = kv.first;
        pair<int, int> range = kv.second;
        cout << "Character: " << c << ", Range: [" << range.first << ", " << range.second << "]" << endl;
    }

    return 0;
}
