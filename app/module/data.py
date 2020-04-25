import subprocess 
import json

class Data :
    def __init__ (self, year, month, proof=False, record=False, npts=False) : 
        self.year = year 
        self.month = month

        self.has_access_to = {
            'proof': proof,
            'record': record,
            'npts': npts
        }

        subprocess.run( ["mkdir", "/_data" ] )
        if proof: self.copy( f"{self.year}-{self.month}-zombies-proof.txt" )
        if record: self.copy( f"{self.year}-{self.month}-record.tar.bz", True )
        if npts: self.copy( f"{self.year}-{self.month}-zombieHunter.tar.bz", True )

    def get_data_from(function) :
        def wrapper(self, file_type) :
            if not self.has_access_to[file_type] :
                print(f"You data interface does not has access to '{file_type}'")
                return 
            else :
                return function(self)
        return wrapper

    def copy(self, file_name, need_extract=False ) :
        file_exist = not subprocess.call(["ls", f"/_data/{file_name}"])
        if file_exist :
            print(f"{file_name} already existed, skip to loading data")
            return 

        subprocess.run( ["cp", f"/archive/{file_name}", f"/_data/{file_name}" ] )
        if need_extract: 
            self.extract(file_name)

    def extract (self, file_name) :
        extract_command = f"tar -C /_data -xzf /_data/{file_name}"
        subprocess.run(extract_command.split())
    
    def get_data (self, file_type) :
        if file_type == 'proof' : return self.get_proof('proof')
        elif file_type == 'npts' : return self.get_npts('npts')
        elif file_type == 'record' : return self.get_record('record')

    @get_data_from
    def get_proof (self) :
        proof = f"{self.year}-{self.month}-zombies-proof.txt"
        f = open(f"/_data/{proof}", "r") 
        return f.readlines()

    @get_data_from
    def get_record (self) :
        data = []
        for i in range(22) :
            if i == 2 or i == 8 or i == 9 or i == 17 :
                continue
            rrc = "{:02d}".format(i)
            file_name = f"/_data/{self.year}-{self.month}-zombie-record-finder-rrc{rrc}.json" 
            with open(file_name)  as f:
                record = json.load(f)
                data.append(record)
        return data

    @get_data_from
    def get_npts(self) :
        data = []
        for p in range(10) :
            f = open(f'/_data/{self.year}-{self.month}-active-route-{p}.txt', 'r')  
            lines = f.readlines() 
            data += lines[1:]
            f.close()
        return data 

    def __del__ (self) :
        del self.year
        del self.month

if __name__=='__main__' :
    print("\n1. Initialize with 2019, 1, npts:True")
    data_interface_npts = Data(2019, 1, npts=True)
    
    print("\n2. Try to get record and proof")
    data_interface_npts.get_data('record')
    data_interface_npts.get_data('proof')

    print("\n3. Try to get npts data")
    data_interface_npts.get_data('npts')