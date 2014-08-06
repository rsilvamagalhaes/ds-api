#pragma once

#ifndef WIN32

#ifndef isfinite
#define isfinite(val) (val <= std::numeric_limits<double>::max())
#endif

#endif

#undef COMPILER
#include "src/v8.h"
#include "src/ast.h"
#include "src/scopes.h"

#include "Wrapper.h"

namespace v8i = v8::internal;

template <typename T>
inline py::object to_python(T *node);

template <typename T>
inline py::list to_python(v8i::ZoneList<T *>* lst);

inline py::object to_python(v8i::Handle<v8i::String> str)
{ 
  if (str.is_null()) return py::object();

  v8i::Vector<const char> buf = str->ToAsciiVector();

  return py::str(buf.start(), buf.length());
}

class CAstScope 
{
  v8i::Scope *m_scope;
public:
  CAstScope(v8i::Scope *scope) : m_scope(scope) {}

  bool is_eval(void) const { return m_scope->is_eval_scope(); }
  bool is_func(void) const { return m_scope->is_function_scope(); }
  bool is_global(void) const { return m_scope->is_global_scope(); }

  bool calls_eval(void) const { return m_scope->calls_eval(); }
  bool outer_scope_calls_eval(void) const { return m_scope->outer_scope_calls_eval(); }

  bool inside_with(void) const { return m_scope->inside_with(); }
  bool contains_with(void) const { return m_scope->contains_with(); }

  py::object outer(void) const { v8i::Scope *scope = m_scope->outer_scope(); return scope ? py::object(CAstScope(scope)) : py::object(); }

  py::list declarations(void) const { return to_python(m_scope->declarations()); }
};

class CAstVariable 
{
  v8i::Variable *m_var;
public:
  CAstVariable(v8i::Variable *var) : m_var(var) {}

  bool IsValidLeftHandSide(void) const { return m_var->IsValidLeftHandSide(); }

  CAstScope scope(void) const { return CAstScope(m_var->scope()); }
  py::object name(void) const { return to_python(m_var->name()); }
  v8i::Variable::Mode mode(void) const { return m_var->mode(); }

  bool is_global(void) const { return m_var->is_global(); }
  bool is_this(void) const { return m_var->is_this(); }
  bool is_arguments(void) const { return m_var->is_arguments(); }
  bool is_possibly_eval(void) const { return m_var->is_possibly_eval(); }
};

class CAstNode
{  
protected:
  v8i::AstNode *m_node;

  CAstNode(v8i::AstNode *node) : m_node(node) {}

  template <typename T>
  T *as(void) const { return static_cast<T *>(m_node); }
public:
  virtual ~CAstNode() {}

  static void Expose(void);
};

class CAstStatement : public CAstNode
{
protected:
  CAstStatement(v8i::Statement *stat) : CAstNode(stat) {}
public:
  operator bool(void) const { return !as<v8i::Statement>()->IsEmpty(); }
  int pos(void) const { return as<v8i::Statement>()->statement_pos(); }
};

class CAstExpression : public CAstNode
{
protected:
  CAstExpression(v8i::Expression *expr) : CAstNode(expr) {}
public:
};

class CAstBreakableStatement : public CAstStatement
{
protected:
  CAstBreakableStatement(v8i::BreakableStatement *stat) : CAstStatement(stat) {}
public:
  bool anonymous(void) const { return as<v8i::BreakableStatement>()->is_target_for_anonymous(); }
};

class CAstBlock : public CAstBreakableStatement
{
public:
  CAstBlock(v8i::Block *block) : CAstBreakableStatement(block) {}
};

class CAstDeclaration : public CAstNode
{
public:
  CAstDeclaration(v8i::Declaration *decl) : CAstNode(decl) {}
};

class CAstIterationStatement : public CAstBreakableStatement
{
protected:
  CAstIterationStatement(v8i::IterationStatement *stat) : CAstBreakableStatement(stat) {}
};

class CAstDoWhileStatement : public CAstIterationStatement
{
public:
  CAstDoWhileStatement(v8i::DoWhileStatement *stat) : CAstIterationStatement(stat) {}
};

class CAstWhileStatement : public CAstIterationStatement
{
public:
  CAstWhileStatement(v8i::WhileStatement *stat) : CAstIterationStatement(stat) {}
};

class CAstForStatement : public CAstIterationStatement
{
public:
  CAstForStatement(v8i::ForStatement *stat) : CAstIterationStatement(stat) {}
};

class CAstForInStatement : public CAstIterationStatement
{
public:
  CAstForInStatement(v8i::ForInStatement *stat) : CAstIterationStatement(stat) {}
};

class CAstExpressionStatement : public CAstStatement
{
public:
  CAstExpressionStatement(v8i::ExpressionStatement *stat) : CAstStatement(stat) {}

  py::object expression(void) const { return to_python(as<v8i::ExpressionStatement>()->expression()); }
};

class CAstContinueStatement : public CAstStatement
{
public:
  CAstContinueStatement(v8i::ContinueStatement *stat) : CAstStatement(stat) {}
};

class CAstBreakStatement : public CAstStatement
{
public:
  CAstBreakStatement(v8i::BreakStatement *stat) : CAstStatement(stat) {}
};

class CAstReturnStatement : public CAstStatement
{
public:
  CAstReturnStatement(v8i::ReturnStatement *stat) : CAstStatement(stat) {}

  py::object expression(void) const { return to_python(as<v8i::ReturnStatement>()->expression()); }
};

class CAstWithEnterStatement : public CAstStatement
{
public:
  CAstWithEnterStatement(v8i::WithEnterStatement *stat) : CAstStatement(stat) {}
};

class CAstWithExitStatement : public CAstStatement
{
public:
  CAstWithExitStatement(v8i::WithExitStatement *stat) : CAstStatement(stat) {}
};

class CAstCaseClause 
{
  v8i::CaseClause *m_clause;
public:
  CAstCaseClause(v8i::CaseClause *clause) : m_clause(clause) {}
};

class CAstSwitchStatement : public CAstBreakableStatement
{
public:
  CAstSwitchStatement(v8i::SwitchStatement *stat) : CAstBreakableStatement(stat) {}
};

class CAstIfStatement : public CAstStatement
{
public:
  CAstIfStatement(v8i::IfStatement *stat) : CAstStatement(stat) {}
};

class CAstTargetCollector : public CAstNode
{
public:
  CAstTargetCollector(v8i::TargetCollector *collector) : CAstNode(collector) {}
};

class CAstTryStatement : public CAstStatement
{
protected:
  CAstTryStatement(v8i::TryStatement *stat) : CAstStatement(stat) {}
public:
};

class CAstTryCatchStatement : public CAstTryStatement
{
public:
  CAstTryCatchStatement(v8i::TryCatchStatement *stat) : CAstTryStatement(stat) {}
};

class CAstTryFinallyStatement : public CAstTryStatement
{
public:
  CAstTryFinallyStatement(v8i::TryFinallyStatement *stat) : CAstTryStatement(stat) {}
};

class CAstDebuggerStatement : public CAstStatement
{
public:
  CAstDebuggerStatement(v8i::DebuggerStatement *stat) : CAstStatement(stat) {}
};

class CAstEmptyStatement : public CAstStatement
{
public:
  CAstEmptyStatement(v8i::EmptyStatement *stat) : CAstStatement(stat) {}
};

class CAstLiteral : public CAstExpression
{
public:
  CAstLiteral(v8i::Literal *lit) : CAstExpression(lit) {}
};

class CAstMaterializedLiteral : public CAstExpression
{
protected:
  CAstMaterializedLiteral(v8i::MaterializedLiteral *lit) : CAstExpression(lit) {}
};

class CAstObjectLiteral : public CAstMaterializedLiteral
{
public:
  CAstObjectLiteral(v8i::ObjectLiteral *lit) : CAstMaterializedLiteral(lit) {}
};

class CAstRegExpLiteral : public CAstMaterializedLiteral
{
public:
  CAstRegExpLiteral(v8i::RegExpLiteral *lit) : CAstMaterializedLiteral(lit) {}
};

class CAstArrayLiteral : public CAstMaterializedLiteral
{
public:
  CAstArrayLiteral(v8i::ArrayLiteral *lit) : CAstMaterializedLiteral(lit) {}
};

class CAstCatchExtensionObject : public CAstExpression
{
public:
  CAstCatchExtensionObject(v8i::CatchExtensionObject *obj) : CAstExpression(obj) {}
};

class CAstVariableProxy : public CAstExpression
{
public:
  CAstVariableProxy(v8i::VariableProxy *proxy) : CAstExpression(proxy) {}

  bool IsValidLeftHandSide(void) const { return as<v8i::VariableProxy>()->IsValidLeftHandSide(); }
  bool IsArguments(void) const { return as<v8i::VariableProxy>()->IsArguments(); }
  py::object name(void) const { return to_python(as<v8i::VariableProxy>()->name()); }
  py::object var(void) const { v8i::Variable *var = as<v8i::VariableProxy>()->var(); return var ? py::object(CAstVariable(var)) : py::object();  }
  bool is_this() const  { return as<v8i::VariableProxy>()->is_this(); }
  bool inside_with() const  { return as<v8i::VariableProxy>()->inside_with(); }
};

class CAstSlot : public CAstExpression
{
public:
  CAstSlot(v8i::Slot *slot) : CAstExpression(slot) {}
};

class CAstProperty : public CAstExpression
{
public:
  CAstProperty(v8i::Property *prop) : CAstExpression(prop) {}
};

class CAstCall : public CAstExpression
{
public:
  CAstCall(v8i::Call *call) : CAstExpression(call) {}

  py::object expression(void) const { return to_python(as<v8i::Call>()->expression()); }
  py::list arguments(void) const { return to_python(as<v8i::Call>()->arguments()); }
  int position(void) const { return as<v8i::Call>()->position(); }
};

class CAstCallNew : public CAstExpression
{
public:
  CAstCallNew(v8i::CallNew *call) : CAstExpression(call) {}

  py::object expression(void) const { return to_python(as<v8i::Call>()->expression()); }
  py::list arguments(void) const { return to_python(as<v8i::Call>()->arguments()); }
  int position(void) const { return as<v8i::Call>()->position(); }
};

class CAstCallRuntime : public CAstExpression
{
public:
  CAstCallRuntime(v8i::CallRuntime *call) : CAstExpression(call) {}

  py::object name(void) const { return to_python(as<v8i::CallRuntime>()->name()); }
  py::list arguments(void) const { return to_python(as<v8i::CallRuntime>()->arguments()); }
  bool is_jsruntime(void) const { return as<v8i::CallRuntime>()->is_jsruntime(); }
};

class CAstUnaryOperation : public CAstExpression
{
public:
  CAstUnaryOperation(v8i::UnaryOperation *op) : CAstExpression(op) {}

  v8i::Token::Value op(void) const { return as<v8i::UnaryOperation>()->op(); }
  py::object expression(void) const { return to_python(as<v8i::UnaryOperation>()->expression()); }
};

class CAstBinaryOperation : public CAstExpression
{
public:
  CAstBinaryOperation(v8i::BinaryOperation *op) : CAstExpression(op) {}

  v8i::Token::Value op(void) const { return as<v8i::BinaryOperation>()->op(); }
  py::object left(void) const { return to_python(as<v8i::BinaryOperation>()->left()); }
  py::object right(void) const { return to_python(as<v8i::BinaryOperation>()->right()); }
};

class CAstCountOperation : public CAstExpression
{
public:
  CAstCountOperation(v8i::CountOperation *op) : CAstExpression(op) {}

  bool is_prefix(void) const { return as<v8i::CountOperation>()->is_prefix(); }
  bool is_postfix(void) const { return as<v8i::CountOperation>()->is_postfix(); }

  v8i::Token::Value op(void) const { return as<v8i::CountOperation>()->op(); }
  v8i::Token::Value binary_op(void) const { return as<v8i::CountOperation>()->binary_op(); }
  py::object expression(void) const { return to_python(as<v8i::CountOperation>()->expression()); }
};

class CAstCompareOperation : public CAstExpression
{
public:
  CAstCompareOperation(v8i::CompareOperation *op) : CAstExpression(op) {}

  v8i::Token::Value op(void) const { return as<v8i::CompareOperation>()->op(); }
  py::object left(void) const { return to_python(as<v8i::CompareOperation>()->left()); }
  py::object right(void) const { return to_python(as<v8i::CompareOperation>()->right()); }

  bool for_loop(void) const { return as<v8i::CompareOperation>()->is_for_loop_condition(); }
};

class CAstConditional : public CAstExpression
{
public:
  CAstConditional(v8i::Conditional *cond) : CAstExpression(cond) {}
};

class CAstAssignment : public CAstExpression
{
public:
  CAstAssignment(v8i::Assignment *assignment) : CAstExpression(assignment) {}
};

class CAstThrow : public CAstExpression
{
public:
  CAstThrow(v8i::Throw *th) : CAstExpression(th) {}
};

class CAstFunctionLiteral : public CAstExpression
{
public:
  CAstFunctionLiteral(v8i::FunctionLiteral *func) : CAstExpression(func) {}

  py::object name(void) const { return to_python(as<v8i::FunctionLiteral>()->name()); }
  CAstScope scope(void) const { return CAstScope(as<v8i::FunctionLiteral>()->scope()); }
  py::list body(void) const { return to_python(as<v8i::FunctionLiteral>()->body()); }

  int start_position(void) const { return as<v8i::FunctionLiteral>()->start_position(); }
  int end_position() const { return as<v8i::FunctionLiteral>()->end_position(); }
  bool is_expression() const { return as<v8i::FunctionLiteral>()->is_expression(); }
};

class CAstFunctionBoilerplateLiteral : public CAstExpression
{
public:
  CAstFunctionBoilerplateLiteral(v8i::FunctionBoilerplateLiteral *func) : CAstExpression(func) {}
};

class CAstThisFunction : public CAstExpression
{
public:
  CAstThisFunction(v8i::ThisFunction *func) : CAstExpression(func) {}
};

struct CAstObjectCollector : public v8i::AstVisitor
{
  py::object m_obj;

#define DECLARE_VISIT(type) virtual void Visit##type(v8i::type* node) { m_obj = py::object(CAst##type(node)); }
  AST_NODE_LIST(DECLARE_VISIT)
#undef DECLARE_VISIT
};

template <typename T>
inline py::object to_python(T *node)
{
  if (!node) return py::object();
  
  CAstObjectCollector collector;

  node->Accept(&collector);

  return collector.m_obj;  
}

struct CAstListCollector : public v8i::AstVisitor
{
  py::list m_nodes;

#define DECLARE_VISIT(type) virtual void Visit##type(v8i::type* node) { m_nodes.append(py::object(CAst##type(node))); }
  AST_NODE_LIST(DECLARE_VISIT)
#undef DECLARE_VISIT
};

template <typename T>
inline py::list to_python(v8i::ZoneList<T *>* lst)
{
  CAstListCollector collector;

  for (int i=0; i<lst->length(); i++)
  {
    lst->at(i)->Accept(&collector);
  }

  return collector.m_nodes;
}
