(define   (problem parking)
  (:domain parking)
  (:objects
     car_00  car_01  car_02  car_03  car_04  car_05  car_06  car_07  car_08  car_09  car_10  car_11  car_12  car_13  car_14  car_15  car_16  car_17  car_18  car_19  car_20  car_21  car_22  car_23  car_24  car_25 - car
     curb_00 curb_01 curb_02 curb_03 curb_04 curb_05 curb_06 curb_07 curb_08 curb_09 curb_10 curb_11 curb_12 curb_13 - curb
  )
  (:init
    (at_curb car_00)
    (at_curb_num car_00 curb_00)
    (behind_car car_24 car_00)
    (car_clear car_24)
    (at_curb car_21)
    (at_curb_num car_21 curb_01)
    (behind_car car_04 car_21)
    (car_clear car_04)
    (at_curb car_03)
    (at_curb_num car_03 curb_02)
    (behind_car car_06 car_03)
    (car_clear car_06)
    (at_curb car_02)
    (at_curb_num car_02 curb_03)
    (behind_car car_22 car_02)
    (car_clear car_22)
    (at_curb car_16)
    (at_curb_num car_16 curb_04)
    (behind_car car_05 car_16)
    (car_clear car_05)
    (at_curb car_15)
    (at_curb_num car_15 curb_05)
    (behind_car car_23 car_15)
    (car_clear car_23)
    (at_curb car_08)
    (at_curb_num car_08 curb_06)
    (behind_car car_20 car_08)
    (car_clear car_20)
    (at_curb car_12)
    (at_curb_num car_12 curb_07)
    (behind_car car_14 car_12)
    (car_clear car_14)
    (at_curb car_18)
    (at_curb_num car_18 curb_08)
    (behind_car car_17 car_18)
    (car_clear car_17)
    (at_curb car_13)
    (at_curb_num car_13 curb_09)
    (behind_car car_25 car_13)
    (car_clear car_25)
    (at_curb car_11)
    (at_curb_num car_11 curb_10)
    (behind_car car_01 car_11)
    (car_clear car_01)
    (at_curb car_19)
    (at_curb_num car_19 curb_11)
    (behind_car car_07 car_19)
    (car_clear car_07)
    (at_curb car_09)
    (at_curb_num car_09 curb_12)
    (behind_car car_10 car_09)
    (car_clear car_10)
    (curb_clear curb_13)
  )
  (:goal
    (and
      (at_curb_num car_00 curb_00)
      (behind_car car_14 car_00)
      (at_curb_num car_01 curb_01)
      (behind_car car_15 car_01)
      (at_curb_num car_02 curb_02)
      (behind_car car_16 car_02)
      (at_curb_num car_03 curb_03)
      (behind_car car_17 car_03)
      (at_curb_num car_04 curb_04)
      (behind_car car_18 car_04)
      (at_curb_num car_05 curb_05)
      (behind_car car_19 car_05)
      (at_curb_num car_06 curb_06)
      (behind_car car_20 car_06)
      (at_curb_num car_07 curb_07)
      (behind_car car_21 car_07)
      (at_curb_num car_08 curb_08)
      (behind_car car_22 car_08)
      (at_curb_num car_09 curb_09)
      (behind_car car_23 car_09)
      (at_curb_num car_10 curb_10)
      (behind_car car_24 car_10)
      (at_curb_num car_11 curb_11)
      (behind_car car_25 car_11)
      (at_curb_num car_12 curb_12)
      (at_curb_num car_13 curb_13)
    )
  )
)
