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

namespace dml {

class DmlAllocator;

// Owns a D3D12 default heap buffer allocated using the DML device's
// allocator. This is essentially a convenience wrapper over a device memory
// allocation as well as the buffer region that spans it. When this object is
// destructed, the device memory is freed to the allocator and the buffer region
// is released.
class DmlBufferImpl {
 public:
  DmlBufferImpl() = default;
  DmlBufferImpl(DmlAllocator* allocator, uint64_t size_in_bytes);
  ~DmlBufferImpl();

  // Move-only
  DmlBufferImpl(const DmlBufferImpl&) = delete;
  DmlBufferImpl& operator=(const DmlBufferImpl&) = delete;
  DmlBufferImpl(DmlBufferImpl&&) = default;
  DmlBufferImpl& operator=(DmlBufferImpl&&) = default;

  uint64_t SizeInBytes() const;
  explicit operator bool() const { return !!buffer_region_; }

 private:
  DmlAllocator* allocator_;  // weak; owned by the DML device factory
  void* ptr_ = nullptr;
  D3D12BufferRegion buffer_region_;

  friend class DmlBuffer;
  friend class DmlBufferAllocator;
};

class DmlBuffer {
 public:
  DmlBuffer() = default;
  ~DmlBuffer();
  explicit DmlBuffer(DmlAllocator* allocator, uint64_t size_in_bytes);

  // Move-only
  DmlBuffer(const DmlBuffer&) = delete;
  DmlBuffer& operator=(const DmlBuffer&) = delete;
  DmlBuffer(DmlBuffer&&) = default;
  DmlBuffer& operator=(DmlBuffer&&) = default;

  ID3D12Resource* Resource() const;
  uint64_t Offset() const;
  uint64_t SizeInBytes() const;

  DML_BUFFER_BINDING GetBufferBinding() const;

  explicit operator bool() const { return !!impl_.buffer_region_; }

 private:
  DmlBufferImpl impl_;
};

}  // namespace tensorflow
