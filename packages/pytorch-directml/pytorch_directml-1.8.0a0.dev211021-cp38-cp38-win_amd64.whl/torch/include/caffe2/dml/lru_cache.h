/* Copyright (c) Microsoft Corporation.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/
#pragma once

#include <list>
#include <map>
#include <mutex>
#include <map>

#include <c10/util/Optional.h>

template<typename T>
class LRUQueue {
  // LRU queue (oldest first) and map of size to LRU queue position
  std::list<T> lru;
  std::map<T, typename std::list<T>::iterator> lru_reference;

public:
  void Remove(const T& key) {
    auto existing_entry = lru_reference.find(key);
    assert(existing_entry != std::end(lru_reference));
    lru.erase(existing_entry->second);
    lru_reference.erase(existing_entry);
  }

  void Update(const T& key) {
    // Insert entry as least likely candidate for removal
    lru.push_back(key);
    const auto& lru_entry = lru_reference.find(key);
    if (lru_entry != std::end(lru_reference)) {
      // Remove existing entry and update lru_reference
      lru.erase(lru_entry->second);
      lru_entry->second = std::prev(lru.end());
    } else {
      lru_reference[key] = std::prev(lru.end());
    }

    assert(lru_reference.size() == lru.size());
  }

  auto RemoveLeastUsed() {
    auto least_used = lru.front();
    lru.pop_front();
    lru_reference.erase(least_used);
    return least_used;
  }
};

template<typename K, typename V, typename VAlloc>
class LRUCache {
  // Thread-safe LRU cache of resources
  // VAlloc must have a Alloc(const K&) -> V method and a Key(const K&) -> c10::optional<K> method
  // V must free its resources at destruction
  std::multimap<K, V> cached_resources;
  LRUQueue<K> lru;
  VAlloc allocator;

  static constexpr size_t max_cached_resources = 512;
  std::recursive_mutex mutex;

public:
  V Alloc(const K& key) {
    {
      // Return a cached entry if possible
      std::unique_lock<std::recursive_mutex> lock(mutex);
      auto resource_it = cached_resources.find(key);
      if (resource_it != std::end(cached_resources)) {
        auto resource = std::move(resource_it->second);
        cached_resources.erase(resource_it);
        if (cached_resources.count(key)) {
          lru.Update(key);
        } else {
          // No more "key" in the cache, so remove from LRU queue
          lru.Remove(key);
        }
        return resource;
      }
    }

    // Not available in cache, allocate new resource
    return allocator.Alloc(key);
  }

  void Free(V&& ptr) {
    c10::optional<K> key = allocator.Key(std::move(ptr));
    if (key) {
      // Add freed entry to cache
      std::unique_lock<std::recursive_mutex> lock(mutex);
      if (cached_resources.size() >= max_cached_resources) {
        // Limit cache size
        cached_resources.erase(lru.RemoveLeastUsed());
      }
      cached_resources.insert({*key, std::move(ptr)});
      lru.Update(*key);
    }
  }
};
