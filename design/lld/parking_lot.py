"""
Ways to appraoch a general design problem
- Use Cases generation: 
    Gather all possible use cases
    Parking can be single-level or multilevel.
    Types of vehicles that can be parked, separate spaces for each type of vehicle.
    Entry and exit points.
- Constraints and analysis:
    How many users, How much data etc.
    Number of vehicles that can be accommodated of any type.
- Basic design:
    Most basic design. Few users case.
    Vehicle/Type of vehicle.
    Entry and Exit points.
    Different spots for vehicles.
- Bottlenecks:
    Find the bottlenecks and solve them.
    Capacity breach for any type of vehicle.
- Scalability:
    A large number of users. 4 and 5 step will go in loop till we get a satisfactory answer.
    Scalable from single-level to multi-level
    Scalable from Bike only parking to accommodate all kinds of vehicles.
"""
# This code need to be refined and checked
# https://github.com/louisdo/ParkingLot/blob/master/system.py

import sqlite3,datetime
conn=sqlite3.connect('ParkingLotDatabase.db')
curs=conn.cursor()

''' Tables
create table ParkingLot(name varchar(20),constraint pk_pkl_name primary key(name))

create table ParkingFloor(inParkingLot varchar(20),floornumber smallint unsigned,constraint pk_pkf_floornum primary key(floornumber),constraint fk_pkf_inpkl foreign key(inParkingLot) references ParkingLot(name))

create table Ticket(
  ticketnumber varchar(20), issueplace varchar(20), arrivetime datetime, departtime datetime, fee float, 
  constraint pk_ticket_num primary key(ticketnumber),
  constraint fk_ticket_place foreign key(issueplace)
  references ParkingLot(name))

create table Vehicle(
  license varchar(20), type varchar(12), ticketnumber varchar(20),inParkingLot varchar(20), inParkingFloor varchar(20),
  constraint pk_v_license primary key(license),
  constraint fk_v_ticketnumber foreign key(ticketnumber)
  references Ticket(ticketnumber),
  constraint fk_v_pkl foreign key(inParkingLot)
  references ParkingLot(name),
  constraint fk_v_pkf foreign key(inParkingFloor)
  references ParkingFloor(floornumber))

create table ParkingSpot
  (spotnumber smallint unsigned,inParkingLot varchar(20), inParkingFloor smallint unsigned,status varchar(10), type varchar(12), vehicle_in_license varchar(20),
  constraint pk_ps_license primary key(vehicle_in_license), 
  constraint fk_ps_inpkl foreign key(inParkingLot)
  references ParkingLot(name)
  constraint fk_ps_inpkf foreign key(inParkingLot)
  references ParkingFloor(floornumber)
  constraint fk_ps_vil foreign key(vehicle_in_license)
  references Vehicle(license))

create table Panel
  (type varchar(12), id integer, inParkingLot,
  constraint fk_panel_inpkl foreign key(inParkingLot)
  references ParkingLot(name))

create table Account
  (username varchar(20), password varchar(20), type varchar(12),
  constraint pk_acc_username primary key(username))

'''
class SQLLiteDemo(object):
  def addParkingLot(name):
    with conn:
      try:
        curs.execute("insert into ParkingLot values(:name)", {'name': name})
      except Exception:
        pass

  def addParkingFloor(parkinglot):
    with conn:
      curs.execute("""
      select max(pkf.floornumber)
      from ParkingFloor pkf inner join ParkingLot pkl
      on pkf.inParkingLot=pkl.name
      where pkf.inParkingLot=:parkinglot
      """,{"parkinglot":parkinglot})
      floornumber,=curs.fetchone()
      if floornumber==None: floornumber=0
      curs.execute("insert into ParkingFloor values(:inParkingLot,:floornumber)",{"inParkingLot":parkinglot,"floornumber":floornumber+1})

  def getParkingFloorNumber(parkinglot):
    with conn:
      curs.execute("select max(floornumber) from ParkingFloor where inParkingLot=:parkinglot",{"parkinglot":parkinglot})
      ret,=curs.fetchone()
      return ret



  def addEntrancePanel(parkinglot):
    with conn:
      curs.execute("select max(id) from Panel where type=:type and inParkingLot=:parkinglot",{"type":"Entrance","parkinglot":parkinglot})
      maxid,=curs.fetchone()
      if not maxid: maxid=1000
      curs.execute("insert into Panel values(:type,:id,:inParkingLot)",{"type":'Entrance',"id":maxid+1,"inParkingLot":parkinglot})

  def addExitPanel(parkinglot):
      with conn:
          curs.execute("select max(id) from Panel where type=:type and inParkingLot=:parkinglot",{"type":'Exit',"parkinglot":parkinglot})
          maxid,=curs.fetchone()
          if not maxid: maxid=2000
          curs.execute("insert into Panel values(:type,:id,:inParkingLot)",{"type":'Exit',"id":maxid+1,"inParkingLot":parkinglot})

  def VehicleInit(licenseNumber,type):
      with conn:
          try:
              curs.execute("insert into Vehicle values(:license,:type,:ticketnumber,:inParkingLot,:inParkingFloor)",
                          {"license":licenseNumber,"type":type,"ticketnumber":None,"inParkingLot":None,"inParkingFloor":None})
          except Exception:
              pass


  def ParkingSpotInit(type,parkingfloor,parkinglot):
      with conn:
          curs.execute("select max(spotnumber) from ParkingSpot where inParkingFloor=:parkingfloor and inParkingLot=:parkinglot",
                      {"parkingfloor":parkingfloor,"parkinglot":parkinglot})
          maxspotnum,=curs.fetchone()
          if not maxspotnum: maxspotnum=0
          curs.execute("insert into ParkingSpot values(:spotnumber,:inParkingLot,:inParkingFloor,:status,:type,:vehicle_in_license)",
                      {"spotnumber":maxspotnum+1,"inParkingLot":parkinglot,"inParkingFloor":parkingfloor,"status":"avail","type":type,"vehicle_in_license":None})


  def addVehicle(licenseNumber,ParkingLotName,ParkingFloorNumber,SpotNumber):
      dict={"Car":"Compact","Electric":"Electric","Truck":"Large","Van":"Large","Motorbike":"Motorbike"}
      with conn:
          curs.execute("select inParkingLot,ticketnumber, type from Vehicle where license=:ln",{"ln":licenseNumber})
          test,test3,test4,=curs.fetchone()
          curs.execute("select type from ParkingSpot where spotnumber=:spotnumber",{"spotnumber":SpotNumber})
          test2,=curs.fetchone()
          if not test and test3 and dict[test4]==test2:
              curs.execute("""
              update Vehicle 
              set inParkingLot=:pklname, inParkingFloor=:pkfnumber
              where license=:ln
              """,{"pklname":ParkingLotName,"pkfnumber":"In floor {}".format(ParkingFloorNumber),"ln":licenseNumber})
              curs.execute("""
                      update ParkingSpot
                      set vehicle_in_license=:licenseNumber, status=:stt
                      where inParkingLot=:Lotname and inParkingFloor=:floornum and spotnumber=:sn
                      """, {"licenseNumber": licenseNumber, "stt": "unavail", "Lotname": ParkingLotName,
                            "floornum": ParkingFloorNumber, "sn": SpotNumber})

  def ParkingTicketInit(ticketNumber,ParkingLotName,licenseNumber,EntrancePanelId):
      with conn:
          curs.execute("select ticketnumber from Vehicle where license=:licenseNumber",
                      {"licenseNumber":licenseNumber})
          test,=curs.fetchone()
          if not test:
              curs.execute("""
              update Vehicle
              set ticketnumber=:ticketNumber
              where license=:licenseNumber
              """,{"ticketNumber":ticketNumber,"licenseNumber":licenseNumber})
              curs.execute("""
              insert into Ticket
              values(:ticketNumber,:issueplace,(select datetime(current_timestamp,'localtime')),:departtime,:fee)
              """,{"ticketNumber":ticketNumber,"issueplace":ParkingLotName+' Entrance Panel id: {}'.format(EntrancePanelId),
                  "departtime":None,"fee":None})

  def GetTicketNumber(license):
      with conn:
          curs.execute("select ticketnumber from Vehicle where license=:license",
                      {"license":license})
          ret,=curs.fetchone()
          return ret

  def ScanTicket(TicketNumber):
      with conn:
          curs.execute("select departtime from Ticket where ticketnumber=:ticketnumber",{"ticketnumber":TicketNumber})
          tn,=curs.fetchone()
          if not tn:
              curs.execute("""
              update Ticket
              set departtime=(select datetime(current_timestamp,'localtime'))
              where ticketnumber=:ticketNumber
              """,{"ticketNumber":TicketNumber})



  def ProcessTicket(ticketNumber):
      with conn:
          curs.execute("""
          select julianday(departtime)-julianday(arrivetime) from Ticket where ticketnumber=:ticketNumber
          """,{"ticketNumber":ticketNumber})
          ret,=curs.fetchone()
          curs.execute("select license from Vehicle where ticketnumber=:ticketNumber",{"ticketNumber":ticketNumber})
          license,=curs.fetchone()
          curs.execute("delete from Vehicle where ticketnumber=:ticketNumber",{"ticketNumber":ticketNumber})
          curs.execute("delete from Ticket where ticketnumber=:ticketNumber",{"ticketNumber":ticketNumber})
          curs.execute("""
          update ParkingSpot
          set status=:stt, vehicle_in_license=:license
          where vehicle_in_license=:licenseCheck
          """,{"stt":'avail',"license":None,"licenseCheck":license})
          return "Your parking fare is {}$".format(round(ret*24,2))


  def AccountInit(username,password,type):
      with conn:
          try:
              curs.execute("""
              insert into Account
              values(:username,:pass,:type)
              """,{"username":username,"pass":password,"type":type})
          except Exception:
              pass

  def displayBoardInit(type,floorNumber,parkinglot):
      with conn:
          curs.execute("select count(spotnumber) from ParkingSpot where type=:type and status=:stt and inParkingFloor=:floorNumber and inParkingLot=:parkinglot",
                      {"type":type,"stt":"avail","floorNumber":floorNumber,"parkinglot":parkinglot.name})
          ret,=curs.fetchone()
          return ret

  def deleteAll():
      with conn:
          curs.execute("delete from ParkingLot")
          curs.execute("delete from ParkingFloor")
          curs.execute("delete from Panel")
          curs.execute("delete from Vehicle")
          curs.execute("delete from ParkingSpot")
          curs.execute("delete from Ticket")



  def show():
      with conn:
          curs.execute("select * from ParkingLot order by name")
          print(curs.fetchall())
          curs.execute("select * from ParkingFloor order by floornumber")
          print(curs.fetchall())
          curs.execute("select * from Panel")
          print(curs.fetchall())
          curs.execute("select * from Vehicle")
          print(curs.fetchall())
          curs.execute("select * from ParkingSpot order by inParkingLot, inParkingFloor")
          print(curs.fetchall())
          curs.execute("select * from Ticket")
          print(curs.fetchall())
          curs.execute("select * from Account")
          print(curs.fetchall())


conn.commit()

import datetime,secrets
import random

sqlite_demo = SQLLiteDemo()

class ParkingLot:
  def __init__(self,name):
    self.name=name
    sqlite_demo.addParkingLot(name)
  def __addParkingFloor(self):
    temp=ParkingFloor(self)
    return temp
  def adminOnly(self):
    return self.__addParkingFloor()
  def addEntrancePanel(self):
    sqlite_demo.addEntrancePanel(self.name)
  def addExitPanel(self):
    sqlite_demo.addExitPanel(self.name)

class EntrancePanel:
  def __init__(self,inParkingLot):
    self.inParkingLot=inParkingLot
    sqlite_demo.addEntrancePanel(inParkingLot)
  def printTicket(self,vehicleObject):
    vehicleObject.assignTicket(self.inParkingLot)
        
class ExitPanel:
    def __init__(self,inParkingLot):
        self.inParkingLot=inParkingLot
        sqlite_demo.addExitPanel(inParkingLot)
    def scanTicket(self,parkingticket,vehicleObject):
        sqlite_demo.ScanTicket(parkingticket.ticketNumber)
    def ProcessPayment(self,parkingticket,payingMethod):
        sqlite_demo.ProcessTicket(parkingticket.ticketNumber)

class ParkingTicket:
    def __init__(self,vehicleObject,parkinglotobject,EntrancePanelId):
        sqlite_demo.ParkingTicketInit(secrets.token_hex(16),parkinglotobject.name,vehicleObject.licenseNumber,EntrancePanelId)
        self.ticketNumber=sqlite_demo.GetTicketNumber(vehicleObject.licenseNumber)

class Payment:
    def __init__(self,parkingTicketobject):
        self.creationDate=parkingTicketobject.issuedAt
        self.amount=parkingTicketobject.payedAmount
        self.status=False
        self.ticket=parkingTicketobject
    def initiateTransaction(self,typeofTrans):
        if typeofTrans=='Credit Card':
            CreditCardTransaction(self.ticket.ticketInfo.licenseNumber).Transaction(self.ticket.payedAmount)
        else:
            CashTransaction(self.ticket.licenseNumber).Transaction(self.ticket.payedAmount)

class CreditCardTransaction:
    def __init__(self,name):
        self.nameOnCard=name
    def Transaction(self,amount):
        print('Successfully payed {}$ by credit card'.format(amount))


class CashTransaction:
    def __init__(self,name):
        self.cashTenderer=name
    def Transaction(self,amount):
        print('Successfully payed {}$ by cash'.format(amount))


class ParkingFloor:
    def __init__(self,parkinglot):
        sqlite_demo.addParkingFloor(parkinglot.name)
        self.name = sqlite_demo.getParkingFloorNumber(parkinglot.name)
        self.inParkingLot=parkinglot
    def addParkingSpot(self,parkingSpotobject):
        temp=parkingSpotobject(self,self.inParkingLot)
        return temp


class ParkingDisplayBoard:
    def __init__(self,parkingfloor,parkinglot):
        #['Handicapped','Compact','Large','Motorbike','Electric']:
        self.handicappedFreeSpot=sqlite_demo.displayBoardInit('Handicapped',parkingfloor,parkinglot)
        self.compactFreeSpot=sqlite_demo.displayBoardInit('Compact',parkingfloor,parkinglot)
        self.largeFreeSpot=sqlite_demo.displayBoardInit('Large',parkingfloor,parkinglot)
        self.motorbikerFreeSpot=sqlite_demo.displayBoardInit('Motorbike',parkingfloor,parkinglot)
        self.electricFreeSpot=sqlite_demo.displayBoardInit('Electric',parkingfloor,parkinglot)
        self.floor=parkingfloor
    def show(self):
        string="""
        Free spots left in floor {}
        
        Handicapped: {} spot(s) left
        Compact:     {} spot(s) left
        Large:       {} spot(s) left
        Motorbike:   {} spot(s) left
        Electric:    {} spot(s) left
        """.format(self.floor,
                   self.handicappedFreeSpot,
                   self.compactFreeSpot,
                   self.largeFreeSpot,
                   self.motorbikerFreeSpot,
                   self.electricFreeSpot)
        print(string)


class ParkingSpot:
    def __init__(self,type,parkingfloor,parkinglotobject):
        self.ParkingLot=parkinglotobject
        self.ParkingFloor=parkingfloor
        self.type=type
        sqlite_demo.ParkingSpotInit(self.type,parkingfloor,parkinglotobject.name)
    
    def addVehicle(self,vehicleObject,SpotNumber):
        sqlite_demo.addVehicle(vehicleObject.licenseNumber,self.ParkingLot.name,self.ParkingFloor.name,SpotNumber)


class HandicappedSpot(ParkingSpot):
    def __init__(self,parkingfloor,parkinglot):
        ParkingSpot.__init__(self,'Handicapped',parkingfloor,parkinglot)

class CompactSpot(ParkingSpot):
    def __init__(self,parkingfloor,parkinglot):
        ParkingSpot.__init__(self,'Compact',parkingfloor,parkinglot)

class LargeSpot(ParkingSpot):
    def __init__(self,parkingfloor,parkinglot):
        ParkingSpot.__init__(self,'Large',parkingfloor,parkinglot)

class MotorbikeSpot(ParkingSpot):
    def __init__(self,parkingfloor,parkinglot):
        ParkingSpot.__init__(self,'Motorbike',parkingfloor,parkinglot)

class ElectricSpot(ParkingSpot):
    def __init__(self,parkingfloor,parkinglot):
        ParkingSpot.__init__(self,'Electric',parkingfloor,parkinglot)


class Vehicle:
    def __init__(self,licenseNumber,type):
        self.licenseNumber=licenseNumber
        self.type=type
        sqlite_demo.VehicleInit(self.licenseNumber,self.type)
    def assignTicket(self,parkinglotobject,EntrancePanelId):
        self.ticket=ParkingTicket(self,parkinglotobject,EntrancePanelId)


class Car(Vehicle):
    def __init__(self,licenseNumber):
        Vehicle.__init__(self,licenseNumber,'Car')

class Truck(Vehicle):
    def __init__(self,licenseNumber):
        Vehicle.__init__(self,licenseNumber,'Truck')

class Electric(Vehicle):
    def __init__(self,licenseNumber):
        Vehicle.__init__(self,licenseNumber,'Electric')

class Van(Vehicle):
    def __init__(self,licenseNumber):
        Vehicle.__init__(self,licenseNumber,'Van')

class Motorbike(Vehicle):
    def __init__(self,licenseNumber):
        Vehicle.__init__(self,licenseNumber,'Motorbike')



class Account:
    def __init__(self,username,password,type):
        self.username=username
        self.password=password
        sqlite_demo.AccountInit(self.username,self.password,type)

class Admin(Account):
    def __init__(self,username,password):
        Account.__init__(self,username,password,self.__class__.__name__)
    def setupParkingLot(self,name,Numberoffloor,enPanelNumber,exPanelNumber):
        pkl = ParkingLot(name)
        for index in range(Numberoffloor):
            pkl.adminOnly()
        for index in range(enPanelNumber):
            pkl.addEntrancePanel()
        for index in range(exPanelNumber):
            pkl.addExitPanel()
        return pkl
    def setupParkingFloor(self,floorNumber,ParkingLot,HandicappedNum,CompactNum,LargeNum,MotorbikeNum,ElectricNum):
        for index in range(HandicappedNum):
            spot = HandicappedSpot(floorNumber, ParkingLot)
        for index in range(CompactNum):
            spot = CompactSpot(floorNumber, ParkingLot)
        for index in range(LargeNum):
            spot = LargeSpot(floorNumber, ParkingLot)
        for index in range(MotorbikeNum):
            spot = MotorbikeSpot(floorNumber, ParkingLot)
        for index in range(ElectricNum):
            spot = ElectricSpot(floorNumber, ParkingLot)

#--------------------------------------------------------------------------------------------
#below are functional functions!





def assignTicketandGetintoSpot(floorNumber,ParkingLotObject,spotNumber,entrancePanelId,VehicleObject):
    VehicleObject.assignTicket(ParkingLotObject,entrancePanelId)
    sqlite_demo.addVehicle(VehicleObject.licenseNumber,ParkingLotObject.name,floorNumber,spotNumber)

def ScanTicketandProcessPayment(ticketNumber):
    try:
        sqlite_demo.ScanTicket(ticketNumber)
        print(sqlite_demo.ProcessTicket(ticketNumber))
    except TypeError:
        print("Ticket not exist!")


# This is a way to use the system(everything would be nicer if I design a GUI but I'm lazy)

if __name__=='__main__':
    admin=Admin("louisdo","lamthon1511")
    pkl=ParkingLot("The Sparks")
    moto=Motorbike("31-297-T9")
    car=Car("30-T4-1975")
    assignTicketandGetintoSpot(1,pkl,151,1001,moto)
    assignTicketandGetintoSpot(2,pkl,51,1001,car)
    ScanTicketandProcessPayment(moto.ticket.ticketNumber)
    board1=ParkingDisplayBoard(1,pkl)
    board2=ParkingDisplayBoard(2,pkl)
    board1.show()
    board2.show()
    sqlite_demo.show()


"""
Basic Code in Java
A very basic parkinglot with barebones...

Model Class(es)

public class Slot
{
    public int Id { get; set; }
    public Size Size { get; set; }
    public bool IsAvailable { get; set; }
}

public enum Size
{
    Small = 1,
    Medium = 2,
    Large = 3
}
Data Access class / Interface:

public interface IParkingLotDataAccess
{
    List<Slot> GetAllAvailable();
    List<Slot> GetAllAvailable(Size size);
    void UpdateSlot(int slotId, bool available);
}

public class ParkingLotDataAccess : IParkingLotDataAccess
{

    private static readonly ConcurrentBag<Slot> allSlots = new ConcurrentBag<Slot>
    {
        new Slot {Size = Size.Small, Id = 1, IsAvailable = true},
        new Slot {Size = Size.Small, Id = 2, IsAvailable = true},

        new Slot {Size = Size.Medium, Id = 11, IsAvailable = true},
        new Slot {Size = Size.Medium, Id = 12, IsAvailable = true},

        new Slot {Size = Size.Large, Id = 21, IsAvailable = true},
        new Slot {Size = Size.Large, Id = 22, IsAvailable = true},
    };

    public List<Slot> GetAllAvailable()
    {
        return allSlots.Where(s => s.IsAvailable).ToList();
    }

    public List<Slot> GetAllAvailable(Size size)
    {
        return allSlots.Where(s => s.Size >= size && s.IsAvailable).ToList();
    }

    public void UpdateSlot(int slotId, bool available)
    {
        allSlots.First(s => s.Id == slotId).IsAvailable = available;
    }
}
Business / Controller classes / interface

public interface IParkingLotManager
{
    int CheckIn(Size vehicleSize);
    bool Checkout(int slotId);

}

public class ParkingLotManager : IParkingLotManager
{
    private readonly IParkingLotDataAccess repo;

    public ParkingLotManager(IParkingLotDataAccess repo)
    {
        this.repo = repo;
    }

    public int CheckIn(Size vehicleSize)
    {
        // get the list of all empty parking lots for given size or bigger

        List<Slot> slots = repo.GetAllAvailable(vehicleSize);
        if (!slots.Any())
        {
            return -1;
        }
		
		// if found one...
		// update the IsAvailable property of that slot
        Slot s = slots.First();
        s.IsAvailable = false;
		
		// save updated slot in the collection of slots
        repo.UpdateSlot(s.Id, false);
		
		// return slot id in case of success, return -1 if no available...
        return s.Id;
    }

    public bool Checkout(int slotId)
    {
        repo.UpdateSlot(slotId, true);
        return true;
    }
}
Again its a very basic class design and here are couple of unit tests:

[TestFixture]
public class ParkingLotManagerTests
{

    private IParkingLotDataAccess repo;
    private IParkingLotManager manager;
    [SetUp]
    public void Setup()
    {
        repo = new ParkingLotDataAccess();
        manager = new ParkingLotManager(repo);
    }

    [Test]
    public void ShouldSuccessfullyCheckInLargeVehicles()
    {
        int id1 = manager.CheckIn(Size.Large);
        int id2 = manager.CheckIn(Size.Large);

        int id3 = manager.CheckIn(Size.Large);

        Assert.AreNotEqual(id1, id2);
        Assert.AreEqual(id3, -1);


        bool result = manager.Checkout(id1);
        Assert.True(result);

        int id4 = manager.CheckIn(Size.Large);
        Assert.AreEqual(id4, id1);
    }


    [Test]
    public void I_Have_Medium_Size_Vehicle_All_MediumSLotsAreEngaged_IShould_Get_Large_Parking_Lot()
    {
        // Arrange.

        repo.UpdateSlot(11, false);
        repo.UpdateSlot(12, false);

        int slotId = manager.CheckIn(Size.Medium);

        Assert.That(slotId, Is.GreaterThanOrEqualTo(21));
        Assert.That(slotId, Is.LessThanOrEqualTo(22));
    }
}
"""