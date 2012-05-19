/*
IntelBras OP4114 driver for MESS
(c)2012 Felipe C. da S. Sanches <juca@members.fsf.org>

Licensed under GNU GPL version 2 (or later).
*/

#define EMULATE_LCD 0

#include "emu.h"
#include "cpu/z180/z180.h"
#include "cpu/mcs51/mcs51.h"
#include "machine/ram.h"
#include "op4114.lh"
#include "rendlay.h"

#if EMULATE_LCD
#include "video/hd44780.h"
#endif

class op4114_state : public driver_device
{
public:
	op4114_state(const machine_config &mconfig, device_type type, const char *tag)
		: driver_device(mconfig, type, tag),
#if EMULATE_LCD
	m_lcdc(*this, "hd44780"),
#endif
  m_maincpu(*this, "maincpu")
  { }

	required_device<cpu_device> m_maincpu;
#if EMULATE_LCD
	required_device<hd44780_device> m_lcdc;
#endif

  DECLARE_READ8_MEMBER(z180_data_r);
#if EMULATE_LCD
  DECLARE_WRITE8_MEMBER(z180_data_w);
#endif

  DECLARE_WRITE8_MEMBER(sidepanel_data_w);
  DECLARE_READ8_MEMBER(sidepanel_p1_r);
  char current_block;
  bool rs, rw;
};

WRITE8_MEMBER( op4114_state::sidepanel_data_w )
{
	//printf("sidepanel main memory write: %.5x data=%.2x\n", offset, data);
  if (offset & 0b1000){
    current_block = data;
  } else {
    for (register char i = 0; i < 8; i++)
	  {
    	char ledname[8];
      sprintf(ledname,"led%d",i + 8*(offset%8));
	    output_set_value(ledname, !BIT(data, 7-i));
    }    
  }
}

READ8_MEMBER( op4114_state::z180_data_r )
{
  if (offset != 0x32)  printf("read z180 from address: %xh\n", offset);
  return 0xff;
}

#if EMULATE_LCD
WRITE8_MEMBER( op4114_state::z180_data_w )
{
  if (offset !=4 && offset !=5){
  	//printf("z180 main memory write: %.5x data=%.2x (%c)\n", offset, data, data);
  }

  switch ((offset >> 1) & 0b111){
    case 3:
      rs = data & 0b1000;
      rw = data & 0b10000;
//      printf("LCD: RS=%s\n", rs ? "0 (Control)" : "1 (Data)");
//      printf("LCD: R/W=%s\n", rw ? "0 (Write)" : "1 (Read)");
      break;

    case 5:
      if (rs){
        //RS=1 -> DATA
        if (rw){
          //RW=1 -> READ
          m_lcdc->data_read(space, offset, data);
        }else{
          //RW=0 -> WRITE
          m_lcdc->data_write(space, offset, data);
        }
      }else{
        //RS=0 -> CONTROL
        if (rw){
          //RW=1 -> READ
          m_lcdc->control_read(space, offset, data);
        }else{
          //RW=0 -> WRITE
          m_lcdc->control_write(space, offset, data);
        }
      }
//      printf("LCD: data=0x%.2x\n", data);
      break;

    default:
      break;
  }
}
#endif 

//maybe keyboard should be emulated by reading external memory address 0b1000
// instead of port 1 ?
READ8_MEMBER( op4114_state::sidepanel_p1_r )
{
  //read the state of the currently selected block of buttons
  static int count=0;
	char ledname[8];

  register int i;
	for (i = 0; i < 8; i++)
	{
		sprintf(ledname,"led%d",i);
		//output_set_value(ledname, BIT(count/100, i));
	}

	//printf("sidepanel P1 read: %.5x\n",(int) count);
  return count++;
}

/* Address maps */
static ADDRESS_MAP_START(op4114_mem, AS_PROGRAM, 8, op4114_state)
    AM_RANGE( 0x0000, 0x1ffff ) AM_ROM AM_REGION("maincpu", 0)
    /* TODO: chute
 AM_RANGE( 0x20000, 0x20fff ) AM_RAM */
ADDRESS_MAP_END

static ADDRESS_MAP_START(op4114_sidepanel_io, AS_IO, 8, op4114_state)
    AM_RANGE( MCS51_PORT_P1, MCS51_PORT_P1 ) AM_READ( sidepanel_p1_r )
    AM_RANGE( 0x0, 0x7 ) AM_WRITE( sidepanel_data_w )
ADDRESS_MAP_END

static ADDRESS_MAP_START(op4114_io, AS_IO, 8, op4114_state)
#if EMULATE_LCD
    AM_RANGE( 0x0, 0x1ffff ) AM_WRITE( z180_data_w )
#endif
    AM_RANGE( 0x0, 0x1ffff ) AM_READ( z180_data_r )
ADDRESS_MAP_END

static MACHINE_RESET( op4114 )
{
	memset(machine.device<ram_device>(RAM_TAG)->pointer(),0,16*1024);

  for (register char i=0; i<8; i++){
    char ledname[8];
    sprintf(ledname,"led%d",i);
    output_set_value(ledname, 1);
    printf("RESET: %.1x\n", i);
  }
}

#if EMULATE_LCD
static PALETTE_INIT( op4114 )
{
	palette_set_color(machine, 0, MAKE_RGB(138, 146, 148));
	palette_set_color(machine, 1, MAKE_RGB(92, 83, 88));
}

static const hd44780_interface op4114_display =
{
	2,					// number of lines
	20,					// chars for line
	NULL				// custom display layout
};

static const gfx_layout op4114_charlayout =
{
	5, 8,	/* 5 x 8 characters */
	256,	/* 256 characters */
	1,	/* 1 bits per pixel */
	{ 0 },	/* no bitplanes */
	{ 3, 4, 5, 6, 7},
	{ 0, 8, 2*8, 3*8, 4*8, 5*8, 6*8, 7*8},
	8*8	/* 8 bytes */
};

static GFXDECODE_START( op4114 )
	GFXDECODE_ENTRY( "hd44780", 0x0000, op4114_charlayout, 0, 1 )
GFXDECODE_END
#endif

/* Input ports */
static INPUT_PORTS_START( op4114 )
INPUT_PORTS_END
 
/* Machine driver */
static MACHINE_CONFIG_START( op4114, op4114_state )
    /* basic machine hardware */
    MCFG_CPU_ADD("maincpu", Z180,  XTAL_16MHz) /* TODO: chute */
    MCFG_CPU_PROGRAM_MAP(op4114_mem)
    MCFG_CPU_IO_MAP(op4114_io)

    MCFG_CPU_ADD("sidepanelcpu", I8051,  XTAL_16MHz) /* TODO: chute */
    MCFG_CPU_IO_MAP(op4114_sidepanel_io)

    MCFG_MACHINE_RESET(op4114)
    
    /* internal ram */
    MCFG_RAM_ADD(RAM_TAG)
    MCFG_RAM_DEFAULT_SIZE("16K")

  	/* video hardware */
#if EMULATE_LCD
    MCFG_SCREEN_ADD("screen", LCD)
  	MCFG_SCREEN_REFRESH_RATE(50)
  	MCFG_SCREEN_VBLANK_TIME(ATTOSECONDS_IN_USEC(2500)) /* not accurate */
  	MCFG_SCREEN_UPDATE_DEVICE("hd44780", hd44780_device, screen_update)
  	MCFG_SCREEN_SIZE(120, 18)
  	MCFG_SCREEN_VISIBLE_AREA(0, 120-1, 0, 18-1)
  	MCFG_PALETTE_LENGTH(2)
  	MCFG_PALETTE_INIT(op4114)
  	MCFG_DEFAULT_LAYOUT(layout_lcd)
  	MCFG_GFXDECODE(op4114)

  	MCFG_HD44780_ADD("hd44780", op4114_display)
#else
    MCFG_DEFAULT_LAYOUT(layout_op4114)
#endif

MACHINE_CONFIG_END

/* ROM definition */
ROM_START( op4114 )
    ROM_REGION( 0x20000, "maincpu", 0 )
    ROM_LOAD( "op4114_main.bin", 0x0000, 0x20000, CRC(2352734c) SHA1(a69bd0397866c1a5e5dac92a9228fc41f41120de) )

    ROM_REGION( 0x8000, "sidepanelcpu", 0 )
    ROM_LOAD( "op4114_sidepanel.bin", 0x0000, 0x8000, CRC(e1b2704e) SHA1(0cfd8e508c63940af86c44fb6bd4b0efdfdf7fa4) )

#if EMULATE_LCD
	ROM_REGION( 0x0860, "hd44780", ROMREGION_ERASE )
	ROM_LOAD( "44780a00.bin",    0x0000, 0x0860,  BAD_DUMP CRC(3a89024c) SHA1(5a87b68422a916d1b37b5be1f7ad0b3fb3af5a8d))
#endif

ROM_END

COMP( 1999, op4114,  0,       0,		op4114,	op4114,	 0, 		"IntelBras",	"Telefone OP-4114",		 GAME_NO_SOUND | GAME_NOT_WORKING)
