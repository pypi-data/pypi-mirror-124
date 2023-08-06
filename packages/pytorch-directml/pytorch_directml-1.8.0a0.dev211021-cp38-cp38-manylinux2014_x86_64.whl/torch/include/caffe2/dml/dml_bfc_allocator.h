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

#include "dml_buffer_region.h"
#include "dml_common.h"
#include "dml_heap_allocator.h"
//#include "tensorflow/core/common_runtime/gpu/gpu_bfc_allocator.h"

namespace dml {

class D3D12HeapAllocator;

class DmlAllocator {
  // A SubAllocator that wraps a D3D12HeapAllocator
  // class SubAllocatorWrapper final {
  //  public:
  //   SubAllocatorWrapper(D3D12HeapAllocator* impl) {}

  //  public:  // SubAllocator overrides
  //   void* Alloc(size_t alignment, size_t num_bytes) {
  //     void* p = impl_->Alloc(num_bytes);
  //     // VisitAlloc(p, 0, num_bytes);
  //     return p;
  //   }

  //   void Free(void* ptr, size_t num_bytes) {
  //     // VisitFree(ptr, 0, num_bytes);
  //     impl_->Free(ptr, num_bytes);
  //   }

  //  private:
  //   D3D12HeapAllocator* impl_;
  // };

 public:
  DmlAllocator(D3D12HeapAllocator* heap_allocator/*,
               uint64_t memory_limit_in_bytes, const GPUOptions& gpu_options,
               const string& name*/);

  void* Alloc(size_t alignment, size_t num_bytes) {
      void* p = heap_allocator_->Alloc(num_bytes);
      // VisitAlloc(p, 0, num_bytes);
      return p;
    }

  void Free(void* ptr, size_t num_bytes) {
    // VisitFree(ptr, 0, num_bytes);
    heap_allocator_->Free(ptr, num_bytes);
  }

  D3D12BufferRegion CreateBufferRegion(const void* ptr, uint64_t size_in_bytes);

 private:
  D3D12HeapAllocator* heap_allocator_;  // not owned
};

}  // namespace tensorflow
