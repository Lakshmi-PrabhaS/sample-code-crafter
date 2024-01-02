// custom_check.cpp
#include <clang/AST/ASTConsumer.h>
#include <clang/AST/RecursiveASTVisitor.h>
#include <clang/Frontend/FrontendActions.h>
#include <clang/Tooling/Tooling.h>

class VariableNamingVisitor
  : public clang::RecursiveASTVisitor<VariableNamingVisitor> {
public:
  bool VisitVarDecl(clang::VarDecl *varDecl) {
    std::string varName = varDecl->getNameAsString();
    if (!varName.empty() && !std::islower(varName[0])) {
      llvm::errs() << "Variable name does not start with lower case: " << varName << "\n";
    }
    return true;
  }
};

class VariableNamingConsumer : public clang::ASTConsumer {
public:
  virtual void HandleTranslationUnit(clang::ASTContext &Context) {
    visitor.TraverseDecl(Context.getTranslationUnitDecl());
  }

private:
  VariableNamingVisitor visitor;
};

class VariableNamingAction : public clang::ASTFrontendAction {
public:
  virtual std::unique_ptr<clang::ASTConsumer> CreateASTConsumer(
    clang::CompilerInstance &Compiler, llvm::StringRef InFile) {
    return std::unique_ptr<clang::ASTConsumer>(
      new VariableNamingConsumer());
  }
};

int main(int argc, char **argv) {
  clang::tooling::runToolOnCode(std::make_unique<VariableNamingAction>(), argv[1]);
  return 0;
}

