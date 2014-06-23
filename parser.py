import csv

from pymongo import MongoClient
from bson import ObjectId

csv_filename = 'kdi-local-elections-observations-first-round-2013.csv'

# Connect to default local instance of mongo
client = MongoClient()

# Get database and collection
db = client.kdi
collection = db.localelectionsfirstround2013

# Clear data
collection.remove({})

def parse_csv():
	'''
	Reads the KDI local election monitoring CSV file.
	Creates Mongo document for each observation entry.
	Stores generated JSON documents.
	'''
	with open(csv_filename, 'rb') as csvfile:
		reader = csv.reader(csvfile)
		
		# Skip the header
		next(reader, None)
		
		# Iterate through the rows, retrieve desired values.
		for row in reader:
			# POLLING STATION
			polling_station_number = row[3] # Column name: nrQV
			room_number = row[4] # Column name: NRVV
			
			commune = row[5] # Column name: Komuna
			polling_station_name = row[6] # Column name: EQV
			
			# VOTING MATERIAL
			material_left_behind = row[7] # Column name: 01gja
			have_physical_access = row[8] # Column name: 02gja
			
			# ARRIVAL TIME
			arrival_time = row[9] # column name: P01KA
			how_to_vote_info = row[10] # column name: P02A
			list_of_candidates = row[11] # column name: P02B
			when_preparation_start = row[12] # column name:P03Perg
			number_KVV_members = row[13] #column name:P04KVV
			female = row[14] #column name:P04Fem
			UV_lamp = row[15] #column name:P05Lla
			spray = row[16] # column name:P05Ngj
			voters_list = row[17] # column name:P05Lis
			ballots = row[18] # column name:P05Flv	
			stamp = row[19] # column name:P05Vul
			ballot_box = row[20] # column name:P05Kut
			voters_book = row[21] # column name:P05Lib
			voting_cabin = row[22] # column name:P05Kab
			envelops_condition_voters = row[23] # column name:P05ZFK
			number_of_accepted_ballots = row[24] # column name:P06NFP
			number_of_voters_in_voting_station_list = row[25] # column name: P07VNL
			number_of_voting_cabins=row[26] # column name:P08NKV
			votingbox_shown_empty=row[27] # column name:P09TKZ
			closed_with_safetystrip = row[28] # column name:P10SHS
			did_they_register_serial_number_of_strips = row[29] # column name:P11NRS
			cabins_provided_voters_safety_and_privancy = row[30] # column name:P12KFV

	
			
			# VOTER INFORMATION
			ultra_violet_control = row[45] # Column name: PV03UVL
			identified_with_document = row[46] # Column name: PV04IDK
			finger_sprayed = row[47] # Column name: PV05GSH
			sealed_ballot = row[48] # Column name: PV06VUL
			
			how_many_voted_by_ten_AM = row[49] # Column name: PV07-10
			how_many_voted_by_one_PM = row[50] # Column name: PV07-13
			how_many_voted_by_four_PM = row[51] # Column name: PV07-16
			how_many_voted_by_seven_PM = row[52] # Column name: PV07-19
			
			# BALLOTS - MUNICIPAL ASSEMBLY ELECTIONS
			total_ballots_mae = row[101] # PAK01
			invalid_ballots_in_box_mae = row[102] # PAK02
			ballots_set_aside_mae = row[103] # PAK03
			# something = row[104] # PAK04
				
			# BALLOTS - MAYOR ELECTIONS
			total_ballots_me = row[105] # PKK01
			invalid_ballots_in_box_me = row[106] # PKK02
			ballots_set_aside_me = row[107] # PKK03
			bollots_put_in_transaparent_bag = row[108] # PKK04
			
			# TODO: Figure out if invalid_ballots_in_box_xxx and ballots_set_aside_xxx are redundant.
			# If invalid_ballots_in_box_xxx and ballots_set_aside_xxx refer to the same thing then we only need to count (invalid_ballots_in_box_xxx) and not the flag (ballots_set_aside_xxx)
			
			#FIXME: When dealing with numbers, set in document as int instead of string.
			#FIXME: Translate PO/YO to True/False boolean values.
			#FIXME: Translate mutlti-choice values to english (e.g. Gjithmone to Always)
			
			observation = {
				'_id': str(ObjectId()),
				'pollingStation':{
					'number': polling_station_number,
					'roomNumber': room_number,
					'name': polling_station_name,
					'commune': commune
				},
				'votingMaterial':{
					'materialLeftBehind': material_left_behind,
					'havePhysicalAccess': have_physical_access
				},
				'arrivalTime':
				{
					

				'Arrival_Time': arrival_time,
					'Voting_materials_placed_in_out_voting_station':{
					'How_to_vote_info': how_to_vote_info,
					'List_of_Candidates': list_of_candidates, 
					'When_Preparation_start': when_preparation_start,
					'Number_KVV_memebers': number_KVV_members, 
					'Female': female, 
					},
				'Was_Necessary_Material_Missing':{
					'UV_Lamp': UV_lamp, 
					'Spray': spray, 
					'Voters_List': voters_list,
					'Ballots': ballots,	
					'Stamp': stamp,
					'Ballot_Box': ballot_box,
					'Voters_Book': voters_book,
					'Voting_Cabin': voting_cabin, 
					'Envelops_Condition_Voters': envelops_condition_voters,
					},
				'Number_of_Accepted_Ballots': number_of_accepted_ballots, 
				'Number_of_voters_in_voting_station_list':number_of_voters_in_voting_station_list,
				'Number_of_voting_cabins':number_of_voting_cabins,
				'Votingbox_shown_empty': votingbox_shown_empty,
				'Closed_with_safetystrip': closed_with_safetystrip, 
				'Did_they_register_serial_number_of_strips': did_they_register_serial_number_of_strips, 
				'Cabins_provided_voters_safety_and_privancy': cabins_provided_voters_safety_and_privancy,

			
			},
				'votingProcess':{
					'voters':{
						'ultraVioletControl': ultra_violet_control,
						'identifiedWithDocument': identified_with_document,
						'fingerSprayed': finger_sprayed,
						'sealedBallot': sealed_ballot,
						'howManyVotedBy':{
							'tenAM': how_many_voted_by_ten_AM,
							'onePM': how_many_voted_by_one_PM,
							'fourPM': how_many_voted_by_four_PM,
							'sevenPM': how_many_voted_by_seven_PM
						}
					}
				},
				'ballots':{
					'municipalAssembly':{
						'total': total_ballots_mae,
						'invalid':{
							'inBallotBox': invalid_ballots_in_box_mae,
							'setAside': ballots_set_aside_mae
						}
					},
					'mayoral':{
						'total': total_ballots_me,
						'invalid':{
							'inBallotBox': invalid_ballots_in_box_me,
							'setAside': ballots_set_aside_me
						},
						'putInTransparentBag': bollots_put_in_transaparent_bag
					}
				}
			}
			
			# Insert document
			collection.insert(observation)

parse_csv()	
