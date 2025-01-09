from DictionaryMutator import ParameterGenerator

def main():
    generator = ParameterGenerator()
    generator.run_generation()
    
    print("====== specific code ======")
    generator.run_generation("CFE_TBL.json", "CFE_TBL_DUMP_REGISTRY_CC")

if __name__ == "__main__":
    main()
