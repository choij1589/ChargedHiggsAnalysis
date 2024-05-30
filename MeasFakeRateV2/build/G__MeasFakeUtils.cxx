// Do NOT change. Changes will be lost next time file is generated

#define R__DICTIONARY_FILENAME G__MeasFakeUtils
#define R__NO_DEPRECATION

/*******************************************************************/
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#define G__DICTIONARY
#include "ROOT/RConfig.hxx"
#include "TClass.h"
#include "TDictAttributeMap.h"
#include "TInterpreter.h"
#include "TROOT.h"
#include "TBuffer.h"
#include "TMemberInspector.h"
#include "TInterpreter.h"
#include "TVirtualMutex.h"
#include "TError.h"

#ifndef G__ROOT
#define G__ROOT
#endif

#include "RtypesImp.h"
#include "TIsAProxy.h"
#include "TFileMergeInfo.h"
#include <algorithm>
#include "TCollectionProxyInfo.h"
/*******************************************************************/

#include "TDataMember.h"

// Header files passed as explicit arguments
#include "/home/choij/workspace/ChargedHiggsAnalysis/MeasFakeRateV2/include/FitMT.h"

// Header files passed via #pragma extra_include

// The generated code does not explicitly qualify STL entities
namespace std {} using namespace std;

namespace ROOT {
   static TClass *FitMT_Dictionary();
   static void FitMT_TClassManip(TClass*);
   static void delete_FitMT(void *p);
   static void deleteArray_FitMT(void *p);
   static void destruct_FitMT(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::FitMT*)
   {
      ::FitMT *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::FitMT));
      static ::ROOT::TGenericClassInfo 
         instance("FitMT", "FitMT.h", 24,
                  typeid(::FitMT), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &FitMT_Dictionary, isa_proxy, 4,
                  sizeof(::FitMT) );
      instance.SetDelete(&delete_FitMT);
      instance.SetDeleteArray(&deleteArray_FitMT);
      instance.SetDestructor(&destruct_FitMT);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::FitMT*)
   {
      return GenerateInitInstanceLocal(static_cast<::FitMT*>(nullptr));
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const ::FitMT*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *FitMT_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal(static_cast<const ::FitMT*>(nullptr))->GetClass();
      FitMT_TClassManip(theClass);
   return theClass;
   }

   static void FitMT_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrapper around operator delete
   static void delete_FitMT(void *p) {
      delete (static_cast<::FitMT*>(p));
   }
   static void deleteArray_FitMT(void *p) {
      delete [] (static_cast<::FitMT*>(p));
   }
   static void destruct_FitMT(void *p) {
      typedef ::FitMT current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class ::FitMT

namespace ROOT {
   static TClass *vectorlETStringgR_Dictionary();
   static void vectorlETStringgR_TClassManip(TClass*);
   static void *new_vectorlETStringgR(void *p = nullptr);
   static void *newArray_vectorlETStringgR(Long_t size, void *p);
   static void delete_vectorlETStringgR(void *p);
   static void deleteArray_vectorlETStringgR(void *p);
   static void destruct_vectorlETStringgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<TString>*)
   {
      vector<TString> *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<TString>));
      static ::ROOT::TGenericClassInfo 
         instance("vector<TString>", -2, "vector", 423,
                  typeid(vector<TString>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &vectorlETStringgR_Dictionary, isa_proxy, 0,
                  sizeof(vector<TString>) );
      instance.SetNew(&new_vectorlETStringgR);
      instance.SetNewArray(&newArray_vectorlETStringgR);
      instance.SetDelete(&delete_vectorlETStringgR);
      instance.SetDeleteArray(&deleteArray_vectorlETStringgR);
      instance.SetDestructor(&destruct_vectorlETStringgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<TString> >()));

      instance.AdoptAlternate(::ROOT::AddClassAlternate("vector<TString>","std::vector<TString, std::allocator<TString> >"));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const vector<TString>*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlETStringgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal(static_cast<const vector<TString>*>(nullptr))->GetClass();
      vectorlETStringgR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlETStringgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlETStringgR(void *p) {
      return  p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) vector<TString> : new vector<TString>;
   }
   static void *newArray_vectorlETStringgR(Long_t nElements, void *p) {
      return p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) vector<TString>[nElements] : new vector<TString>[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlETStringgR(void *p) {
      delete (static_cast<vector<TString>*>(p));
   }
   static void deleteArray_vectorlETStringgR(void *p) {
      delete [] (static_cast<vector<TString>*>(p));
   }
   static void destruct_vectorlETStringgR(void *p) {
      typedef vector<TString> current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class vector<TString>

namespace ROOT {
   static TClass *maplETStringcOdoublegR_Dictionary();
   static void maplETStringcOdoublegR_TClassManip(TClass*);
   static void *new_maplETStringcOdoublegR(void *p = nullptr);
   static void *newArray_maplETStringcOdoublegR(Long_t size, void *p);
   static void delete_maplETStringcOdoublegR(void *p);
   static void deleteArray_maplETStringcOdoublegR(void *p);
   static void destruct_maplETStringcOdoublegR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const map<TString,double>*)
   {
      map<TString,double> *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(map<TString,double>));
      static ::ROOT::TGenericClassInfo 
         instance("map<TString,double>", -2, "map", 100,
                  typeid(map<TString,double>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &maplETStringcOdoublegR_Dictionary, isa_proxy, 0,
                  sizeof(map<TString,double>) );
      instance.SetNew(&new_maplETStringcOdoublegR);
      instance.SetNewArray(&newArray_maplETStringcOdoublegR);
      instance.SetDelete(&delete_maplETStringcOdoublegR);
      instance.SetDeleteArray(&deleteArray_maplETStringcOdoublegR);
      instance.SetDestructor(&destruct_maplETStringcOdoublegR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::MapInsert< map<TString,double> >()));

      instance.AdoptAlternate(::ROOT::AddClassAlternate("map<TString,double>","std::map<TString, double, std::less<TString>, std::allocator<std::pair<TString const, double> > >"));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const map<TString,double>*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *maplETStringcOdoublegR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal(static_cast<const map<TString,double>*>(nullptr))->GetClass();
      maplETStringcOdoublegR_TClassManip(theClass);
   return theClass;
   }

   static void maplETStringcOdoublegR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_maplETStringcOdoublegR(void *p) {
      return  p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) map<TString,double> : new map<TString,double>;
   }
   static void *newArray_maplETStringcOdoublegR(Long_t nElements, void *p) {
      return p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) map<TString,double>[nElements] : new map<TString,double>[nElements];
   }
   // Wrapper around operator delete
   static void delete_maplETStringcOdoublegR(void *p) {
      delete (static_cast<map<TString,double>*>(p));
   }
   static void deleteArray_maplETStringcOdoublegR(void *p) {
      delete [] (static_cast<map<TString,double>*>(p));
   }
   static void destruct_maplETStringcOdoublegR(void *p) {
      typedef map<TString,double> current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class map<TString,double>

namespace ROOT {
   static TClass *maplETStringcOTH1DmUgR_Dictionary();
   static void maplETStringcOTH1DmUgR_TClassManip(TClass*);
   static void *new_maplETStringcOTH1DmUgR(void *p = nullptr);
   static void *newArray_maplETStringcOTH1DmUgR(Long_t size, void *p);
   static void delete_maplETStringcOTH1DmUgR(void *p);
   static void deleteArray_maplETStringcOTH1DmUgR(void *p);
   static void destruct_maplETStringcOTH1DmUgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const map<TString,TH1D*>*)
   {
      map<TString,TH1D*> *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(map<TString,TH1D*>));
      static ::ROOT::TGenericClassInfo 
         instance("map<TString,TH1D*>", -2, "map", 100,
                  typeid(map<TString,TH1D*>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &maplETStringcOTH1DmUgR_Dictionary, isa_proxy, 0,
                  sizeof(map<TString,TH1D*>) );
      instance.SetNew(&new_maplETStringcOTH1DmUgR);
      instance.SetNewArray(&newArray_maplETStringcOTH1DmUgR);
      instance.SetDelete(&delete_maplETStringcOTH1DmUgR);
      instance.SetDeleteArray(&deleteArray_maplETStringcOTH1DmUgR);
      instance.SetDestructor(&destruct_maplETStringcOTH1DmUgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::MapInsert< map<TString,TH1D*> >()));

      instance.AdoptAlternate(::ROOT::AddClassAlternate("map<TString,TH1D*>","std::map<TString, TH1D*, std::less<TString>, std::allocator<std::pair<TString const, TH1D*> > >"));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const map<TString,TH1D*>*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *maplETStringcOTH1DmUgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal(static_cast<const map<TString,TH1D*>*>(nullptr))->GetClass();
      maplETStringcOTH1DmUgR_TClassManip(theClass);
   return theClass;
   }

   static void maplETStringcOTH1DmUgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_maplETStringcOTH1DmUgR(void *p) {
      return  p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) map<TString,TH1D*> : new map<TString,TH1D*>;
   }
   static void *newArray_maplETStringcOTH1DmUgR(Long_t nElements, void *p) {
      return p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) map<TString,TH1D*>[nElements] : new map<TString,TH1D*>[nElements];
   }
   // Wrapper around operator delete
   static void delete_maplETStringcOTH1DmUgR(void *p) {
      delete (static_cast<map<TString,TH1D*>*>(p));
   }
   static void deleteArray_maplETStringcOTH1DmUgR(void *p) {
      delete [] (static_cast<map<TString,TH1D*>*>(p));
   }
   static void destruct_maplETStringcOTH1DmUgR(void *p) {
      typedef map<TString,TH1D*> current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class map<TString,TH1D*>

namespace ROOT {
   static TClass *maplETStringcORooRealVarmUgR_Dictionary();
   static void maplETStringcORooRealVarmUgR_TClassManip(TClass*);
   static void *new_maplETStringcORooRealVarmUgR(void *p = nullptr);
   static void *newArray_maplETStringcORooRealVarmUgR(Long_t size, void *p);
   static void delete_maplETStringcORooRealVarmUgR(void *p);
   static void deleteArray_maplETStringcORooRealVarmUgR(void *p);
   static void destruct_maplETStringcORooRealVarmUgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const map<TString,RooRealVar*>*)
   {
      map<TString,RooRealVar*> *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(map<TString,RooRealVar*>));
      static ::ROOT::TGenericClassInfo 
         instance("map<TString,RooRealVar*>", -2, "map", 100,
                  typeid(map<TString,RooRealVar*>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &maplETStringcORooRealVarmUgR_Dictionary, isa_proxy, 0,
                  sizeof(map<TString,RooRealVar*>) );
      instance.SetNew(&new_maplETStringcORooRealVarmUgR);
      instance.SetNewArray(&newArray_maplETStringcORooRealVarmUgR);
      instance.SetDelete(&delete_maplETStringcORooRealVarmUgR);
      instance.SetDeleteArray(&deleteArray_maplETStringcORooRealVarmUgR);
      instance.SetDestructor(&destruct_maplETStringcORooRealVarmUgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::MapInsert< map<TString,RooRealVar*> >()));

      instance.AdoptAlternate(::ROOT::AddClassAlternate("map<TString,RooRealVar*>","std::map<TString, RooRealVar*, std::less<TString>, std::allocator<std::pair<TString const, RooRealVar*> > >"));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const map<TString,RooRealVar*>*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *maplETStringcORooRealVarmUgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal(static_cast<const map<TString,RooRealVar*>*>(nullptr))->GetClass();
      maplETStringcORooRealVarmUgR_TClassManip(theClass);
   return theClass;
   }

   static void maplETStringcORooRealVarmUgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_maplETStringcORooRealVarmUgR(void *p) {
      return  p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) map<TString,RooRealVar*> : new map<TString,RooRealVar*>;
   }
   static void *newArray_maplETStringcORooRealVarmUgR(Long_t nElements, void *p) {
      return p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) map<TString,RooRealVar*>[nElements] : new map<TString,RooRealVar*>[nElements];
   }
   // Wrapper around operator delete
   static void delete_maplETStringcORooRealVarmUgR(void *p) {
      delete (static_cast<map<TString,RooRealVar*>*>(p));
   }
   static void deleteArray_maplETStringcORooRealVarmUgR(void *p) {
      delete [] (static_cast<map<TString,RooRealVar*>*>(p));
   }
   static void destruct_maplETStringcORooRealVarmUgR(void *p) {
      typedef map<TString,RooRealVar*> current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class map<TString,RooRealVar*>

namespace ROOT {
   static TClass *maplETStringcORooHistPdfmUgR_Dictionary();
   static void maplETStringcORooHistPdfmUgR_TClassManip(TClass*);
   static void *new_maplETStringcORooHistPdfmUgR(void *p = nullptr);
   static void *newArray_maplETStringcORooHistPdfmUgR(Long_t size, void *p);
   static void delete_maplETStringcORooHistPdfmUgR(void *p);
   static void deleteArray_maplETStringcORooHistPdfmUgR(void *p);
   static void destruct_maplETStringcORooHistPdfmUgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const map<TString,RooHistPdf*>*)
   {
      map<TString,RooHistPdf*> *ptr = nullptr;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(map<TString,RooHistPdf*>));
      static ::ROOT::TGenericClassInfo 
         instance("map<TString,RooHistPdf*>", -2, "map", 100,
                  typeid(map<TString,RooHistPdf*>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &maplETStringcORooHistPdfmUgR_Dictionary, isa_proxy, 0,
                  sizeof(map<TString,RooHistPdf*>) );
      instance.SetNew(&new_maplETStringcORooHistPdfmUgR);
      instance.SetNewArray(&newArray_maplETStringcORooHistPdfmUgR);
      instance.SetDelete(&delete_maplETStringcORooHistPdfmUgR);
      instance.SetDeleteArray(&deleteArray_maplETStringcORooHistPdfmUgR);
      instance.SetDestructor(&destruct_maplETStringcORooHistPdfmUgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::MapInsert< map<TString,RooHistPdf*> >()));

      instance.AdoptAlternate(::ROOT::AddClassAlternate("map<TString,RooHistPdf*>","std::map<TString, RooHistPdf*, std::less<TString>, std::allocator<std::pair<TString const, RooHistPdf*> > >"));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal(static_cast<const map<TString,RooHistPdf*>*>(nullptr)); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *maplETStringcORooHistPdfmUgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal(static_cast<const map<TString,RooHistPdf*>*>(nullptr))->GetClass();
      maplETStringcORooHistPdfmUgR_TClassManip(theClass);
   return theClass;
   }

   static void maplETStringcORooHistPdfmUgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_maplETStringcORooHistPdfmUgR(void *p) {
      return  p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) map<TString,RooHistPdf*> : new map<TString,RooHistPdf*>;
   }
   static void *newArray_maplETStringcORooHistPdfmUgR(Long_t nElements, void *p) {
      return p ? ::new(static_cast<::ROOT::Internal::TOperatorNewHelper*>(p)) map<TString,RooHistPdf*>[nElements] : new map<TString,RooHistPdf*>[nElements];
   }
   // Wrapper around operator delete
   static void delete_maplETStringcORooHistPdfmUgR(void *p) {
      delete (static_cast<map<TString,RooHistPdf*>*>(p));
   }
   static void deleteArray_maplETStringcORooHistPdfmUgR(void *p) {
      delete [] (static_cast<map<TString,RooHistPdf*>*>(p));
   }
   static void destruct_maplETStringcORooHistPdfmUgR(void *p) {
      typedef map<TString,RooHistPdf*> current_t;
      (static_cast<current_t*>(p))->~current_t();
   }
} // end of namespace ROOT for class map<TString,RooHistPdf*>

namespace {
  void TriggerDictionaryInitialization_libMeasFakeUtils_Impl() {
    static const char* headers[] = {
"/home/choij/workspace/ChargedHiggsAnalysis/MeasFakeRateV2/include/FitMT.h",
nullptr
    };
    static const char* includePaths[] = {
"/home/choij/workspace/ChargedHiggsAnalysis/MeasFakeRateV2",
"/home/choij/miniconda3/envs/pyg/include/",
"/home/choij/workspace/ChargedHiggsAnalysis/MeasFakeRateV2/build/",
nullptr
    };
    static const char* fwdDeclCode = R"DICTFWDDCLS(
#line 1 "libMeasFakeUtils dictionary forward declarations' payload"
#pragma clang diagnostic ignored "-Wkeyword-compat"
#pragma clang diagnostic ignored "-Wignored-attributes"
#pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
extern int __Cling_AutoLoading_Map;
class __attribute__((annotate("$clingAutoload$/home/choij/workspace/ChargedHiggsAnalysis/MeasFakeRateV2/include/FitMT.h")))  FitMT;
)DICTFWDDCLS";
    static const char* payloadCode = R"DICTPAYLOAD(
#line 1 "libMeasFakeUtils dictionary payload"


#define _BACKWARD_BACKWARD_WARNING_H
// Inline headers
#include "/home/choij/workspace/ChargedHiggsAnalysis/MeasFakeRateV2/include/FitMT.h"

#undef  _BACKWARD_BACKWARD_WARNING_H
)DICTPAYLOAD";
    static const char* classesHeaders[] = {
"FitMT", payloadCode, "@",
nullptr
};
    static bool isInitialized = false;
    if (!isInitialized) {
      TROOT::RegisterModule("libMeasFakeUtils",
        headers, includePaths, payloadCode, fwdDeclCode,
        TriggerDictionaryInitialization_libMeasFakeUtils_Impl, {}, classesHeaders, /*hasCxxModule*/false);
      isInitialized = true;
    }
  }
  static struct DictInit {
    DictInit() {
      TriggerDictionaryInitialization_libMeasFakeUtils_Impl();
    }
  } __TheDictionaryInitializer;
}
void TriggerDictionaryInitialization_libMeasFakeUtils() {
  TriggerDictionaryInitialization_libMeasFakeUtils_Impl();
}
