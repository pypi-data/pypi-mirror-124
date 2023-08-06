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

#include "dml_buffer.h"
#include "dml_buffer_region.h"
#include "dml_common.h"

namespace dml {

struct DmlBackend;

template <DML_OPERATOR_TYPE TType> struct DmlOperatorTraits;
template <> struct DmlOperatorTraits<DML_OPERATOR_MAX_POOLING1> {  using T = DML_MAX_POOLING1_OPERATOR_DESC; };
// binary ops
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_DIVIDE> { using T = DML_ELEMENT_WISE_DIVIDE_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_MULTIPLY> { using T = DML_ELEMENT_WISE_MULTIPLY_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_ADD> { using T = DML_ELEMENT_WISE_ADD_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_ADD1> { using T = DML_ELEMENT_WISE_ADD1_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_SUBTRACT> { using T = DML_ELEMENT_WISE_SUBTRACT_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_MAX> { using T = DML_ELEMENT_WISE_MAX_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_MIN> { using T = DML_ELEMENT_WISE_MIN_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ACTIVATION_SIGMOID> { using T = DML_ACTIVATION_SIGMOID_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_MODULUS_TRUNCATE> { using T = DML_ELEMENT_WISE_MODULUS_TRUNCATE_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_LOGICAL_GREATER_THAN_OR_EQUAL> { using T = DML_ELEMENT_WISE_LOGICAL_GREATER_THAN_OR_EQUAL_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_LOGICAL_LESS_THAN_OR_EQUAL> { using T = DML_ELEMENT_WISE_LOGICAL_LESS_THAN_OR_EQUAL_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_LOGICAL_GREATER_THAN> { using T = DML_ELEMENT_WISE_LOGICAL_GREATER_THAN_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_LOGICAL_LESS_THAN> { using T = DML_ELEMENT_WISE_LOGICAL_LESS_THAN_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_LOGICAL_EQUALS> { using T = DML_ELEMENT_WISE_LOGICAL_EQUALS_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_LOGICAL_AND> { using T = DML_ELEMENT_WISE_LOGICAL_AND_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_LOGICAL_OR> { using T = DML_ELEMENT_WISE_LOGICAL_OR_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_LOGICAL_XOR> { using T = DML_ELEMENT_WISE_LOGICAL_XOR_OPERATOR_DESC; };
//
template <> struct DmlOperatorTraits<DML_OPERATOR_GEMM> { using T = DML_GEMM_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_REDUCE> { using T = DML_REDUCE_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ACTIVATION_RELU> { using T = DML_ACTIVATION_RELU_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ACTIVATION_LOG_SOFTMAX> { using T = DML_ACTIVATION_LOG_SOFTMAX_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_ASIN> { using T = DML_ELEMENT_WISE_ASIN_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_ATAN> { using T = DML_ELEMENT_WISE_ATAN_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_CEIL> { using T = DML_ELEMENT_WISE_CEIL_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_EXP> { using T = DML_ELEMENT_WISE_EXP_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_FLOOR> { using T = DML_ELEMENT_WISE_FLOOR_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_LOG> { using T = DML_ELEMENT_WISE_LOG_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_COS> { using T = DML_ELEMENT_WISE_COS_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_TAN> { using T = DML_ELEMENT_WISE_TAN_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_CONSTANT_POW> { using T = DML_ELEMENT_WISE_CONSTANT_POW_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_RECIP> { using T = DML_ELEMENT_WISE_RECIP_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_SIN> { using T = DML_ELEMENT_WISE_SIN_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_SQRT> { using T = DML_ELEMENT_WISE_SQRT_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_ERF> { using T = DML_ELEMENT_WISE_ERF_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_SINH> { using T = DML_ELEMENT_WISE_SINH_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_COSH> { using T = DML_ELEMENT_WISE_COSH_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_TANH> { using T = DML_ELEMENT_WISE_TANH_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_ASINH> { using T = DML_ELEMENT_WISE_ASINH_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_ACOSH> { using T = DML_ELEMENT_WISE_ACOSH_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_ATANH> { using T = DML_ELEMENT_WISE_ATANH_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_IDENTITY> { using T = DML_ELEMENT_WISE_IDENTITY_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_IF> { using T = DML_ELEMENT_WISE_IF_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_ABS> { using T = DML_ELEMENT_WISE_ABS_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_ACOS> { using T = DML_ELEMENT_WISE_ACOS_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_LOGICAL_NOT> { using T = DML_ELEMENT_WISE_LOGICAL_NOT_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_CONVOLUTION> { using T = DML_CONVOLUTION_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_AVERAGE_POOLING> { using T = DML_AVERAGE_POOLING_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ACTIVATION_THRESHOLDED_RELU> { using T = DML_ACTIVATION_THRESHOLDED_RELU_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_FILL_VALUE_SEQUENCE> { using T = DML_FILL_VALUE_SEQUENCE_OPERATOR_DESC ; };
template <> struct DmlOperatorTraits<DML_OPERATOR_FILL_VALUE_CONSTANT> { using T = DML_FILL_VALUE_CONSTANT_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_JOIN> { using T = DML_JOIN_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_MAX_POOLING_GRAD> { using T = DML_MAX_POOLING_GRAD_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_AVERAGE_POOLING_GRAD> { using T = DML_AVERAGE_POOLING_GRAD_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_CAST> { using T = DML_CAST_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ACTIVATION_LEAKY_RELU> { using T = DML_ACTIVATION_LEAKY_RELU_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_CLIP> { using T = DML_ELEMENT_WISE_CLIP_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_RESAMPLE> { using T = DML_RESAMPLE_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_RESAMPLE_GRAD> { using T = DML_RESAMPLE_GRAD_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_BIT_AND> { using T = DML_ELEMENT_WISE_BIT_AND_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_NONZERO_COORDINATES> { using T = DML_NONZERO_COORDINATES_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_TILE> { using T = DML_TILE_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_POW> { using T = DML_ELEMENT_WISE_POW_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_ROUND> { using T = DML_ELEMENT_WISE_ROUND_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_ELEMENT_WISE_SIGN> { using T = DML_ELEMENT_WISE_SIGN_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_REVERSE_SUBSEQUENCES> { using T = DML_REVERSE_SUBSEQUENCES_OPERATOR_DESC; };
template <> struct DmlOperatorTraits<DML_OPERATOR_TOP_K1> { using T = DML_TOP_K1_OPERATOR_DESC; };

template <DML_OPERATOR_TYPE TType>
using DML_OP_DESC = typename DmlOperatorTraits<TType>::T;

struct DmlOperatorBase {
  DmlOperatorBase(DmlBackend* backend, const DML_OPERATOR_DESC& op_desc, size_t num_inputs, size_t num_outputs);
  DmlOperatorBase(DmlBackend* backend, IDMLCompiledOperator* compiled_op, size_t num_inputs, size_t num_outputs);

  void AssignInput(size_t index, const D3D12BufferRegion& buffer);
  void AssignOutput(size_t index, const D3D12BufferRegion& buffer);
  const DML_BUFFER_BINDING* GetPersistentResourceBinding() const;  
  void Compute();

 private:
  void Initialize();
  bool IsGraphOp();

 protected:
  DmlBackend* backend_;
  const DML_OPERATOR_DESC op_desc_;

  std::vector<D3D12BufferRegion> inputs_;
  std::vector<D3D12BufferRegion> outputs_;

  Microsoft::WRL::ComPtr<IDMLCompiledOperator> compiled_op_;
  std::unique_ptr<DmlBuffer> persistent_resource_;
  DML_BUFFER_BINDING persistent_resource_binding_;

  bool is_initialized_ = false;
};

// DmlOperator
template <DML_OPERATOR_TYPE TType> struct DmlOperator;

// Output-Only Operators
template <DML_OPERATOR_TYPE TType>
struct DmlOutputOperator : public DmlOperatorBase
{
  DmlOutputOperator(DmlBackend* backend, const DML_OP_DESC<TType>& op_desc) :
    DmlOperatorBase(backend, DML_OPERATOR_DESC {TType, &op_desc}, 0, 1)
  {}

  auto OutputTensor(D3D12BufferRegion buffer) {
    AssignOutput(0, buffer);
  }
};

template <> struct DmlOperator<DML_OPERATOR_FILL_VALUE_SEQUENCE> : DmlOutputOperator<DML_OPERATOR_FILL_VALUE_SEQUENCE> {
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_FILL_VALUE_SEQUENCE>& op_desc) :
     DmlOutputOperator<DML_OPERATOR_FILL_VALUE_SEQUENCE>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_FILL_VALUE_CONSTANT> : DmlOutputOperator<DML_OPERATOR_FILL_VALUE_CONSTANT> {
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_FILL_VALUE_CONSTANT>& op_desc) :
     DmlOutputOperator<DML_OPERATOR_FILL_VALUE_CONSTANT>(backend, op_desc) {}
};

// Binary Operators
template <DML_OPERATOR_TYPE TType>
struct DmlBinaryOperator : public DmlOperatorBase
{
  DmlBinaryOperator(DmlBackend* backend, const DML_OP_DESC<TType>& op_desc) :
    DmlOperatorBase(backend, DML_OPERATOR_DESC {TType, &op_desc}, 2, 1)
  {}

  auto ATensor(D3D12BufferRegion buffer) {
    AssignInput(0, buffer);
  }
  auto BTensor(D3D12BufferRegion buffer) {
    AssignInput(1, buffer);
  }
  auto OutputTensor(D3D12BufferRegion buffer) {
    AssignOutput(0, buffer);
  }
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_DIVIDE> : DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_DIVIDE> {
  DmlOperator(DmlBackend* backend, const DML_ELEMENT_WISE_DIVIDE_OPERATOR_DESC& op_desc) :
     DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_DIVIDE>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_MULTIPLY> : DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_MULTIPLY> {
  DmlOperator(DmlBackend* backend, const DML_ELEMENT_WISE_MULTIPLY_OPERATOR_DESC& op_desc) :
     DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_MULTIPLY>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_ADD> : DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_ADD> {
  DmlOperator(DmlBackend* backend, const DML_ELEMENT_WISE_ADD_OPERATOR_DESC& op_desc) :
     DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_ADD>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_SUBTRACT> : DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_SUBTRACT> {
  DmlOperator(DmlBackend* backend, const DML_ELEMENT_WISE_SUBTRACT_OPERATOR_DESC& op_desc) :
     DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_SUBTRACT>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_MAX> : DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_MAX> {
  DmlOperator(DmlBackend* backend, const DML_ELEMENT_WISE_MAX_OPERATOR_DESC& op_desc) :
     DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_MAX>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_MIN> : DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_MIN> {
  DmlOperator(DmlBackend* backend, const DML_ELEMENT_WISE_MIN_OPERATOR_DESC& op_desc) :
     DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_MIN>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_ADD1> : DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_ADD1> {
  DmlOperator(DmlBackend* backend, const DML_ELEMENT_WISE_ADD1_OPERATOR_DESC& op_desc) :
     DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_ADD1>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_MODULUS_TRUNCATE> : DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_MODULUS_TRUNCATE> {
  DmlOperator(DmlBackend* backend, const DML_ELEMENT_WISE_MODULUS_TRUNCATE_OPERATOR_DESC& op_desc) :
     DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_MODULUS_TRUNCATE>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_LOGICAL_GREATER_THAN_OR_EQUAL> : DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_LOGICAL_GREATER_THAN_OR_EQUAL> {
  DmlOperator(DmlBackend* backend, const DML_ELEMENT_WISE_LOGICAL_GREATER_THAN_OR_EQUAL_OPERATOR_DESC& op_desc) :
     DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_LOGICAL_GREATER_THAN_OR_EQUAL>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_LOGICAL_LESS_THAN_OR_EQUAL> : DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_LOGICAL_LESS_THAN_OR_EQUAL> {
  DmlOperator(DmlBackend* backend, const DML_ELEMENT_WISE_LOGICAL_LESS_THAN_OR_EQUAL_OPERATOR_DESC& op_desc) :
     DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_LOGICAL_LESS_THAN_OR_EQUAL>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_LOGICAL_GREATER_THAN> : DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_LOGICAL_GREATER_THAN> {
  DmlOperator(DmlBackend* backend, const DML_ELEMENT_WISE_LOGICAL_GREATER_THAN_OPERATOR_DESC& op_desc) :
     DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_LOGICAL_GREATER_THAN>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_LOGICAL_LESS_THAN> : DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_LOGICAL_LESS_THAN> {
  DmlOperator(DmlBackend* backend, const DML_ELEMENT_WISE_LOGICAL_LESS_THAN_OPERATOR_DESC& op_desc) :
     DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_LOGICAL_LESS_THAN>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_LOGICAL_EQUALS> : DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_LOGICAL_EQUALS> {
  DmlOperator(DmlBackend* backend, const DML_ELEMENT_WISE_LOGICAL_EQUALS_OPERATOR_DESC& op_desc) :
     DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_LOGICAL_EQUALS>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_LOGICAL_AND> : DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_LOGICAL_AND> {
  DmlOperator(DmlBackend* backend, const DML_ELEMENT_WISE_LOGICAL_AND_OPERATOR_DESC& op_desc) :
     DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_LOGICAL_AND>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_LOGICAL_OR> : DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_LOGICAL_OR> {
  DmlOperator(DmlBackend* backend, const DML_ELEMENT_WISE_LOGICAL_OR_OPERATOR_DESC& op_desc) :
     DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_LOGICAL_OR>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_LOGICAL_XOR> : DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_LOGICAL_XOR> {
  DmlOperator(DmlBackend* backend, const DML_ELEMENT_WISE_LOGICAL_XOR_OPERATOR_DESC& op_desc) :
     DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_LOGICAL_XOR>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_BIT_AND> : DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_BIT_AND> {
  DmlOperator(DmlBackend* backend, const DML_ELEMENT_WISE_BIT_AND_OPERATOR_DESC& op_desc) :
     DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_BIT_AND>(backend, op_desc) {}
}; 

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_POW> : private DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_POW> {
  DmlOperator(DmlBackend* backend, const DML_ELEMENT_WISE_POW_OPERATOR_DESC& op_desc) :
     DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_POW>(backend, op_desc) {}

  auto InputTensor(D3D12BufferRegion buffer) {
    ATensor(buffer);
  }

  auto ExponentTensor(D3D12BufferRegion buffer) {
    BTensor(buffer);
  }

  auto OutputTensor(D3D12BufferRegion buffer) {
    DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_POW>::OutputTensor(buffer);
  }

  auto Compute() {
    DmlBinaryOperator<DML_OPERATOR_ELEMENT_WISE_POW>::Compute();
  }
};

template <> struct DmlOperator<DML_OPERATOR_REVERSE_SUBSEQUENCES> : private DmlBinaryOperator<DML_OPERATOR_REVERSE_SUBSEQUENCES> {
  DmlOperator(DmlBackend* backend, const DML_REVERSE_SUBSEQUENCES_OPERATOR_DESC& op_desc) :
     DmlBinaryOperator<DML_OPERATOR_REVERSE_SUBSEQUENCES>(backend, op_desc) {}

  auto InputTensor(D3D12BufferRegion buffer) {
    ATensor(buffer);
  }

  auto SequenceLengthsTensor(D3D12BufferRegion buffer) {
    BTensor(buffer);
  }

  auto OutputTensor(D3D12BufferRegion buffer) {
    DmlBinaryOperator<DML_OPERATOR_REVERSE_SUBSEQUENCES>::OutputTensor(buffer);
  }

  auto Compute() {
    DmlBinaryOperator<DML_OPERATOR_REVERSE_SUBSEQUENCES>::Compute();
  }
};

// Unary Ops
template <DML_OPERATOR_TYPE TType>
struct DmlUnaryOperator : public DmlOperatorBase
{
  DmlUnaryOperator(DmlBackend* backend, const DML_OP_DESC<TType>& op_desc) :
    DmlOperatorBase(backend, DML_OPERATOR_DESC {TType, &op_desc}, 1, 1)
  {}

  auto InputTensor(D3D12BufferRegion buffer) {
    AssignInput(0, buffer);
  }

  auto OutputTensor(D3D12BufferRegion buffer) {
    AssignOutput(0, buffer);
  }
};
 
template <> struct DmlOperator<DML_OPERATOR_CAST> : DmlUnaryOperator<DML_OPERATOR_CAST> {
  DmlOperator(DmlBackend* backend, const DML_CAST_OPERATOR_DESC& op_desc) :
     DmlUnaryOperator<DML_OPERATOR_CAST>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_TILE> : DmlUnaryOperator<DML_OPERATOR_TILE> {
  DmlOperator(DmlBackend* backend, const DML_TILE_OPERATOR_DESC& op_desc) :
     DmlUnaryOperator<DML_OPERATOR_TILE>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_AVERAGE_POOLING> : DmlUnaryOperator<DML_OPERATOR_AVERAGE_POOLING> {
  DmlOperator(DmlBackend* backend, const DML_AVERAGE_POOLING_OPERATOR_DESC& op_desc) :
     DmlUnaryOperator<DML_OPERATOR_AVERAGE_POOLING>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ACTIVATION_RELU> : DmlUnaryOperator<DML_OPERATOR_ACTIVATION_RELU> {
  DmlOperator(DmlBackend* backend, const DML_ACTIVATION_RELU_OPERATOR_DESC& op_desc) :
     DmlUnaryOperator<DML_OPERATOR_ACTIVATION_RELU>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ACTIVATION_LOG_SOFTMAX> : DmlUnaryOperator<DML_OPERATOR_ACTIVATION_LOG_SOFTMAX> {
  DmlOperator(DmlBackend* backend, const DML_ACTIVATION_LOG_SOFTMAX_OPERATOR_DESC& op_desc) :
     DmlUnaryOperator<DML_OPERATOR_ACTIVATION_LOG_SOFTMAX>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_ASIN> : DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_ASIN> { 
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ELEMENT_WISE_ASIN>& op_desc) :
    DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_ASIN>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_ATAN> : DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_ATAN> { 
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ELEMENT_WISE_ATAN>& op_desc) :
    DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_ATAN>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_CEIL> : DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_CEIL> { 
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ELEMENT_WISE_CEIL>& op_desc) :
    DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_CEIL>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_EXP> : DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_EXP> { 
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ELEMENT_WISE_EXP>& op_desc) :
    DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_EXP>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_ROUND> : DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_ROUND> { 
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ELEMENT_WISE_ROUND>& op_desc) :
    DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_ROUND>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_SIGN> : DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_SIGN> { 
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ELEMENT_WISE_SIGN>& op_desc) :
    DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_SIGN>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_FLOOR> : DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_FLOOR> { 
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ELEMENT_WISE_FLOOR>& op_desc) :
    DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_FLOOR>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_LOG> : DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_LOG> { 
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ELEMENT_WISE_LOG>& op_desc) :
    DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_LOG>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_COS> : DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_COS> { 
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ELEMENT_WISE_COS>& op_desc) :
    DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_COS>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_TAN> : DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_TAN> { 
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ELEMENT_WISE_TAN>& op_desc) :
    DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_TAN>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_CONSTANT_POW> : DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_CONSTANT_POW> { 
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ELEMENT_WISE_CONSTANT_POW>& op_desc) :
    DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_CONSTANT_POW>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_RECIP> : DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_RECIP> { 
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ELEMENT_WISE_RECIP>& op_desc) :
    DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_RECIP>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_SIN> : DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_SIN> { 
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ELEMENT_WISE_SIN>& op_desc) :
    DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_SIN>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_SQRT> : DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_SQRT> { 
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ELEMENT_WISE_SQRT>& op_desc) :
    DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_SQRT>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_ERF> : DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_ERF> { 
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ELEMENT_WISE_ERF>& op_desc) :
    DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_ERF>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_SINH> : DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_SINH> { 
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ELEMENT_WISE_SINH>& op_desc) :
    DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_SINH>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_COSH> : DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_COSH> { 
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ELEMENT_WISE_COSH>& op_desc) :
    DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_COSH>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_TANH> : DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_TANH> { 
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ELEMENT_WISE_TANH>& op_desc) :
    DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_TANH>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_ASINH> : DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_ASINH> { 
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ELEMENT_WISE_ASINH>& op_desc) :
    DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_ASINH>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_LOGICAL_NOT> : DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_LOGICAL_NOT> { 
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ELEMENT_WISE_LOGICAL_NOT>& op_desc) :
    DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_LOGICAL_NOT>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_ACOSH> : DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_ACOSH> { 
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ELEMENT_WISE_ACOSH>& op_desc) :
    DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_ACOSH>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_ATANH> : DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_ATANH> { 
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ELEMENT_WISE_ATANH>& op_desc) :
    DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_ATANH>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_IDENTITY> : DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_IDENTITY> { 
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ELEMENT_WISE_IDENTITY>& op_desc) :
    DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_IDENTITY>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_ABS> : DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_ABS> { 
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ELEMENT_WISE_ABS>& op_desc) :
    DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_ABS>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_ACOS> : DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_ACOS> { 
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ELEMENT_WISE_ACOS>& op_desc) :
    DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_ACOS>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_REDUCE> : DmlUnaryOperator<DML_OPERATOR_REDUCE> { 
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_REDUCE>& op_desc) :
    DmlUnaryOperator<DML_OPERATOR_REDUCE>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ACTIVATION_SIGMOID> : DmlUnaryOperator<DML_OPERATOR_ACTIVATION_SIGMOID> { 
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ACTIVATION_SIGMOID>& op_desc) :
    DmlUnaryOperator<DML_OPERATOR_ACTIVATION_SIGMOID>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ACTIVATION_LEAKY_RELU> : DmlUnaryOperator<DML_OPERATOR_ACTIVATION_LEAKY_RELU> {
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ACTIVATION_LEAKY_RELU>& op_desc) :
     DmlUnaryOperator<DML_OPERATOR_ACTIVATION_LEAKY_RELU>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_CLIP> : DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_CLIP> {
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ELEMENT_WISE_CLIP>& op_desc) :
     DmlUnaryOperator<DML_OPERATOR_ELEMENT_WISE_CLIP>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_RESAMPLE> : DmlUnaryOperator<DML_OPERATOR_RESAMPLE> {
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_RESAMPLE>& op_desc) :
     DmlUnaryOperator<DML_OPERATOR_RESAMPLE>(backend, op_desc) {}
};

template <> struct DmlOperator<DML_OPERATOR_RESAMPLE_GRAD> : DmlUnaryOperator<DML_OPERATOR_RESAMPLE_GRAD> {
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_RESAMPLE_GRAD>& op_desc) :
     DmlUnaryOperator<DML_OPERATOR_RESAMPLE_GRAD>(backend, op_desc) {}
};

template <>
struct DmlOperator<DML_OPERATOR_ELEMENT_WISE_IF> : public DmlOperatorBase
{
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ELEMENT_WISE_IF>& op_desc) :
    DmlOperatorBase(backend, DML_OPERATOR_DESC {DML_OPERATOR_ELEMENT_WISE_IF, &op_desc}, 3, 1)
  {}

  auto ConditionTensor(D3D12BufferRegion buffer) {
    AssignInput(0, buffer);
  }
  auto ATensor(D3D12BufferRegion buffer) {
    AssignInput(1, buffer);
  }
  auto BTensor(D3D12BufferRegion buffer) {
    AssignInput(2, buffer);
  }
  auto OutputTensor(D3D12BufferRegion buffer) {
    AssignOutput(0, buffer);
  }
};

template <>
struct DmlOperator<DML_OPERATOR_MAX_POOLING1> : public DmlOperatorBase
{
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_MAX_POOLING1>& op_desc) :
    DmlOperatorBase(backend, DML_OPERATOR_DESC {DML_OPERATOR_MAX_POOLING1, &op_desc}, 1, 2)
  {}

  auto InputTensor(D3D12BufferRegion buffer) {
    AssignInput(0, buffer);
  }
  auto OutputTensor(D3D12BufferRegion buffer) {
    AssignOutput(0, buffer);
  }
  auto OutputIndicesTensor(D3D12BufferRegion buffer) {
    AssignOutput(1, buffer);
  }
};

template <>
struct DmlOperator<DML_OPERATOR_GEMM> : public DmlOperatorBase
{
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_GEMM>& op_desc) :
    DmlOperatorBase(backend, DML_OPERATOR_DESC {DML_OPERATOR_GEMM, &op_desc}, 3, 1)
  {}

  auto ATensor(D3D12BufferRegion buffer) {
    AssignInput(0, buffer);
  }

  auto BTensor(D3D12BufferRegion buffer) {
    AssignInput(1, buffer);
  }

  auto CTensor(D3D12BufferRegion buffer) {
    AssignInput(2, buffer);
  }

  auto OutputTensor(D3D12BufferRegion buffer) {
    AssignOutput(0, buffer);
  }
};

template <>
struct DmlOperator<DML_OPERATOR_CONVOLUTION> : public DmlOperatorBase
{
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_CONVOLUTION>& op_desc) :
    DmlOperatorBase(backend, DML_OPERATOR_DESC {DML_OPERATOR_CONVOLUTION, &op_desc}, 3, 1)
  {}

  auto InputTensor(D3D12BufferRegion buffer) {
    AssignInput(0, buffer);
  }

  auto FilterTensor(D3D12BufferRegion buffer) {
    AssignInput(1, buffer);
  }

  auto BiasTensor(D3D12BufferRegion buffer) {
    AssignInput(2, buffer);
  }

  auto OutputTensor(D3D12BufferRegion buffer) {
    AssignOutput(0, buffer);
  }
};

template <>
struct DmlOperator<DML_OPERATOR_ACTIVATION_THRESHOLDED_RELU> : public DmlOperatorBase
{
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_ACTIVATION_THRESHOLDED_RELU>& op_desc) :
    DmlOperatorBase(backend, DML_OPERATOR_DESC{DML_OPERATOR_ACTIVATION_THRESHOLDED_RELU,&op_desc}, 1,1)
  {}

  auto InputTensor(D3D12BufferRegion buffer) {
    AssignInput(0, buffer);
  }

  auto OutputTensor(D3D12BufferRegion buffer) {
    AssignOutput(0, buffer);
  }
};

template <>
struct DmlOperator<DML_OPERATOR_JOIN> : public DmlOperatorBase
{
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_JOIN>& op_desc) :
    DmlOperatorBase(backend, DML_OPERATOR_DESC{DML_OPERATOR_JOIN,&op_desc}, op_desc.InputCount, 1)
  {}

  auto InputTensorAtIndex(size_t index, D3D12BufferRegion buffer) {
    AssignInput(index, buffer);
  }

  auto OutputTensor(D3D12BufferRegion buffer) {
    AssignOutput(0, buffer);
  }
};

template <>
struct DmlOperator<DML_OPERATOR_MAX_POOLING_GRAD> : public DmlOperatorBase
{
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_MAX_POOLING_GRAD>& op_desc) :
    DmlOperatorBase(backend, DML_OPERATOR_DESC{DML_OPERATOR_MAX_POOLING_GRAD,&op_desc}, 2, 1)
  {}

  auto InputTensor(D3D12BufferRegion buffer) {
    AssignInput(0, buffer);
  }

  auto InputGradientTensor(D3D12BufferRegion buffer) {
    AssignInput(1, buffer);
  }

  auto OutputGradientTensor(D3D12BufferRegion buffer) {
    AssignOutput(0, buffer);
  }
};

template <>
struct DmlOperator<DML_OPERATOR_AVERAGE_POOLING_GRAD> : public DmlOperatorBase
{
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_AVERAGE_POOLING_GRAD>& op_desc) :
    DmlOperatorBase(backend, DML_OPERATOR_DESC{DML_OPERATOR_AVERAGE_POOLING_GRAD,&op_desc}, 1, 1)
  {}

  auto InputGradientTensor(D3D12BufferRegion buffer) {
    AssignInput(0, buffer);
  }

  auto OutputGradientTensor(D3D12BufferRegion buffer) {
    AssignOutput(0, buffer);
  }
};

template <>
struct DmlOperator<DML_OPERATOR_NONZERO_COORDINATES> : public DmlOperatorBase
{
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_NONZERO_COORDINATES>& op_desc) :
    DmlOperatorBase(backend, DML_OPERATOR_DESC{DML_OPERATOR_NONZERO_COORDINATES,&op_desc}, 1, 2)
  {}

  auto InputTensor(D3D12BufferRegion buffer) {
    AssignInput(0, buffer);
  }

  auto OutputCountTensor(D3D12BufferRegion buffer) {
    AssignOutput(0, buffer);
  }

  auto OutputCoordinatesTensor(D3D12BufferRegion buffer) {
    AssignOutput(1, buffer);
  }
};

template <>
struct DmlOperator<DML_OPERATOR_TOP_K1> : public DmlOperatorBase
{
  DmlOperator(DmlBackend* backend, const DML_OP_DESC<DML_OPERATOR_TOP_K1>& op_desc) :
    DmlOperatorBase(backend, DML_OPERATOR_DESC{DML_OPERATOR_TOP_K1,&op_desc}, 1, 2)
  {}

  auto InputTensor(D3D12BufferRegion buffer) {
    AssignInput(0, buffer);
  }

  auto OutputValueTensor(D3D12BufferRegion buffer) {
    AssignOutput(0, buffer);
  }

  auto OutputIndexTensor(D3D12BufferRegion buffer) {
    AssignOutput(1, buffer);
  }
};
}  // namespace dml