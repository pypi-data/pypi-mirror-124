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

#include "dml_common.h"
#include "dml_operator.h"

namespace dml {

class HardwareAdapter;
class DmlExecutionContext;
class DmlEventQueue;
class D3D12HeapAllocator;
class DmlAllocator;
class DmlUploadHeap;
class DmlReadbackHeap;
class DmlKernelManager;

// Holds device state that is shared across one or more DmlDevice instances.
// Instances of these state objects are owned by the DML device factory.
// Typically one of these state objects exists for each physical D3D adapter,
// but multiple TF DmlDevice instances can share this state. All objects owned
// by this state object are thread-safe.
struct DmlBackend {
 public:
  static std::unique_ptr<DmlBackend> Create(const HardwareAdapter& adapter);

  template<DML_OPERATOR_TYPE TType>
  DmlOperator<TType> CreateOperator(const DML_OP_DESC<TType>& op_desc) {
    return DmlOperator<TType>(this, op_desc);
  }

  DmlOperatorBase CreateOperator(IDMLCompiledOperator* compiled_op, size_t num_inputs, size_t num_outputs) {
    return DmlOperatorBase(this, compiled_op, num_inputs, num_outputs);
  }

  DmlBackend();
  ~DmlBackend();

  std::unique_ptr<HardwareAdapter> adapter;
  Microsoft::WRL::ComPtr<ID3D12Device> d3d_device;
  Microsoft::WRL::ComPtr<ID3D12CommandQueue> command_queue;
  Microsoft::WRL::ComPtr<ID3D12SharingContract> sharing_contract;
  Microsoft::WRL::ComPtr<IDMLDevice> dml_device;
  std::unique_ptr<DmlExecutionContext> execution_context;
  std::unique_ptr<DmlEventQueue> event_queue;
  std::unique_ptr<D3D12HeapAllocator> heap_allocator;
  std::unique_ptr<DmlAllocator> dml_allocator;
  std::unique_ptr<DmlUploadHeap> upload_heap;
  std::unique_ptr<DmlReadbackHeap> readback_heap;
  std::unique_ptr<DmlKernelManager> kernel_manager;
};

}  // namespace dml