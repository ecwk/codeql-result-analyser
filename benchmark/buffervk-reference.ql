import cpp

class BufferVkBufferAccessCall extends FunctionCall {
  BufferVkBufferAccessCall() {
    this.getType().getName() = "BufferHelper &" and
    this.getTarget().getDeclaringType().getQualifiedName() = "rx::BufferVk"
  }
}

from AssignExpr e, BufferVkBufferAccessCall fc, FieldAccess fa
where
  fc.getEnclosingStmt().(ExprStmt).getExpr() = e and
  (
    e.getRValue().(AddressOfExpr).getOperand() = fc
    or
    e.getRValue() = fc
  ) and
  fa.getEnclosingStmt().(ExprStmt).getExpr() = e
select fc,
  "BufferVk::mBuffer is accessed through a function call to $@. The result is assigned to $@::$@.",
  fc.getTarget(), fc.getTarget().getName(), fa.getTarget().getDeclaringType(),
  fa.getTarget().getDeclaringType().getName(), fa.getTarget(), fa.getTarget().getName()