from .layers import *
from .fast_layers import *


def affine_relu_forward(x, w, b):
    """Convenience layer that performs an affine transform followed by a ReLU.

    Inputs:
    - x: Input to the affine layer
    - w, b: Weights for the affine layer

    Returns a tuple of:
    - out: Output from the ReLU
    - cache: Object to give to the backward pass
    """
    a, fc_cache = affine_forward(x, w, b)
    out, relu_cache = relu_forward(a)
    cache = (fc_cache, relu_cache)
    return out, cache

def affine_relu_backward(dout, cache):
    """Backward pass for the affine-relu convenience layer.
    """
    fc_cache, relu_cache = cache
    da = relu_backward(dout, relu_cache)
    dx, dw, db = affine_backward(da, fc_cache)
    return dx, dw, db

# *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

pass

# *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

def affine_bn_relu_forward(x, w, b, gamma, beta, bn_param):
  # Forward pass for affine layer
  a, fc_cache = affine_forward(x, w, b)
  if a is None:
        raise ValueError("Output of affine_forward is None")
  
  # Foward pass for the batch normalization layer
  bn, bn_cache = batchnorm_forward(a, gamma, beta, bn_param)
  if bn is None:
        raise ValueError("Output of batchnorm_forward is None")
  
  # Forward pass for the ReLU activation
  out, relu_cache = relu_forward(bn)
  if out is None:
        raise ValueError("Output of relu_forward is None")
  
  cache = (fc_cache, bn_cache, relu_cache)
  
  return out, cache

def affine_bn_relu_backward(dout, cache):
    """
    Backward pass for the affine -> batchnorm -> ReLU layer.

    Inputs:
    - dout: Upstream derivatives
    - cache: Tuple of:
      - fc_cache: Cache from the affine layer
      - bn_cache: Cache from the batchnorm layer
      - relu_cache: Cache from the ReLU layer

    Returns a tuple of:
    - dx: Gradient with respect to x
    - dw: Gradient with respect to w
    - db: Gradient with respect to b
    - dgamma: Gradient with respect to gamma (batch normalization parameter)
    - dbeta: Gradient with respect to beta (batch normalization parameter)
    """
    fc_cache, bn_cache, relu_cache = cache

    # Backprop through ReLU
    da = relu_backward(dout, relu_cache)
    
    # Backprop through batch normalization
    dx_bn, dgamma, dbeta = batchnorm_backward_alt(da, bn_cache)
    
    # Backprop through affine layer
    dx, dw, db = affine_backward(dx_bn, fc_cache)

    return dx, dw, db, dgamma, dbeta

def affine_ln_relu_forward(x, w, b, gamma, beta, ln_param):
  # Forward pass for affine layer
  a, fc_cache = affine_forward(x, w, b)
  
  # Forward pass for the batch normalization layer
  ln, ln_cache = layernorm_forward(a, gamma, beta, ln_param)
  
  # Forward pass for ReLU activation
  out, relu_cache = relu_forward(ln)
  
  cache = (fc_cache, ln_cache, relu_cache)
  
  return out, cache

def affine_ln_relu_backward(dout, cache):
    """
    Backward pass for the affine -> layernorm -> ReLU layer.

    Inputs:
    - dout: Upstream derivatives
    - cache: Tuple of:
      - fc_cache: Cache from the affine layer
      - ln_cache: Cache from the layernorm layer
      - relu_cache: Cache from the ReLU layer

    Returns a tuple of:
    - dx: Gradient with respect to x
    - dw: Gradient with respect to w
    - db: Gradient with respect to b
    - dgamma: Gradient with respect to gamma (layer normalization parameter)
    - dbeta: Gradient with respect to beta (layer normalization parameter)
    """
    fc_cache, ln_cache, relu_cache = cache

    # Backprop through ReLU
    da = relu_backward(dout, relu_cache)

    # Backprop through layer normalization
    dx_ln, dgamma, dbeta = layernorm_backward(da, ln_cache)

    # Backprop through affine layer
    dx, dw, db = affine_backward(dx_ln, fc_cache)

    return dx, dw, db, dgamma, dbeta

def conv_relu_forward(x, w, b, conv_param):
    """A convenience layer that performs a convolution followed by a ReLU.

    Inputs:
    - x: Input to the convolutional layer
    - w, b, conv_param: Weights and parameters for the convolutional layer

    Returns a tuple of:
    - out: Output from the ReLU
    - cache: Object to give to the backward pass
    """
    a, conv_cache = conv_forward_fast(x, w, b, conv_param)
    out, relu_cache = relu_forward(a)
    cache = (conv_cache, relu_cache)
    return out, cache


def conv_relu_backward(dout, cache):
    """Backward pass for the conv-relu convenience layer.
    """
    conv_cache, relu_cache = cache
    da = relu_backward(dout, relu_cache)
    dx, dw, db = conv_backward_fast(da, conv_cache)
    return dx, dw, db


def conv_bn_relu_forward(x, w, b, gamma, beta, conv_param, bn_param):
    """Convenience layer that performs a convolution, a batch normalization, and a ReLU.

    Inputs:
    - x: Input to the convolutional layer
    - w, b, conv_param: Weights and parameters for the convolutional layer
    - pool_param: Parameters for the pooling layer
    - gamma, beta: Arrays of shape (D2,) and (D2,) giving scale and shift
      parameters for batch normalization.
    - bn_param: Dictionary of parameters for batch normalization.

    Returns a tuple of:
    - out: Output from the pooling layer
    - cache: Object to give to the backward pass
    """
    a, conv_cache = conv_forward_fast(x, w, b, conv_param)
    an, bn_cache = spatial_batchnorm_forward(a, gamma, beta, bn_param)
    out, relu_cache = relu_forward(an)
    cache = (conv_cache, bn_cache, relu_cache)
    return out, cache


def conv_bn_relu_backward(dout, cache):
    """Backward pass for the conv-bn-relu convenience layer.
    """
    conv_cache, bn_cache, relu_cache = cache
    dan = relu_backward(dout, relu_cache)
    da, dgamma, dbeta = spatial_batchnorm_backward(dan, bn_cache)
    dx, dw, db = conv_backward_fast(da, conv_cache)
    return dx, dw, db, dgamma, dbeta


def conv_relu_pool_forward(x, w, b, conv_param, pool_param):
    """Convenience layer that performs a convolution, a ReLU, and a pool.

    Inputs:
    - x: Input to the convolutional layer
    - w, b, conv_param: Weights and parameters for the convolutional layer
    - pool_param: Parameters for the pooling layer

    Returns a tuple of:
    - out: Output from the pooling layer
    - cache: Object to give to the backward pass
    """
    a, conv_cache = conv_forward_fast(x, w, b, conv_param)
    s, relu_cache = relu_forward(a)
    out, pool_cache = max_pool_forward_fast(s, pool_param)
    cache = (conv_cache, relu_cache, pool_cache)
    return out, cache


def conv_relu_pool_backward(dout, cache):
    """Backward pass for the conv-relu-pool convenience layer.
    """
    conv_cache, relu_cache, pool_cache = cache
    ds = max_pool_backward_fast(dout, pool_cache)
    da = relu_backward(ds, relu_cache)
    dx, dw, db = conv_backward_fast(da, conv_cache)
    return dx, dw, db