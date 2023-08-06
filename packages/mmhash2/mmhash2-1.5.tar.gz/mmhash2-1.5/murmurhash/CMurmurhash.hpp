#ifndef MURMURHASH_HPP
#define MURMURHASH_HPP

#include <cstdint>
#include <cstddef>
#include <string>
#include <map>
#include <cmath>

namespace mmhash {

class CMurmurhash {
private:
    std::string dict;
    std::map<char, uint64_t> flipDict;

    static uint64_t pow(uint64_t x, uint64_t y) {
        uint64_t r = 1;
        for (uint64_t i = 0; i < y; i++) {
            r *= x;
        }

        return r;
    }
public:
    CMurmurhash() : dict("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIGKLMNOPQRSTUVWXYZ") {
        for (uint64_t i = 0; i < 62; i++) {
            flipDict[this->dict[i]] = i;
        }
    }
    std::string dechex(uint64_t from);
    std::string base62encode(uint64_t from);
    uint64_t base62decode(std::string from);
    uint64_t hash64a(const void* key, size_t len, unsigned int seed);
    uint64_t hash64b(const void* key, size_t len, unsigned int seed);
};
}

#endif
